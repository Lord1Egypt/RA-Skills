package cli

import (
	"encoding/json"
	"fmt"
	"strings"
	"time"

	"github.com/spf13/cobra"

	"github.com/stozo04/google-health-cli/internal/api"
)

// newDataCmd is the generic data-point surface: `data list <type>` reads any of
// the Google Health data types. Writes are intentionally absent — this tool is
// read-only.
func newDataCmd(app *App) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "data",
		Short: "Read data points for any Google Health data type",
		Args:  cobra.NoArgs,
		RunE: func(c *cobra.Command, _ []string) error {
			return c.Help()
		},
	}
	cmd.AddCommand(newDataListCmd(app))
	return cmd
}

// newDataListCmd lists data points for one data type over a time window,
// emitting the raw API JSON array on stdout (the verbatim records, so an agent
// parses exactly what the API returned). A one-line count goes to stderr.
func newDataListCmd(app *App) *cobra.Command {
	var (
		date   string
		days   int
		from   string
		to     string
		all    bool
		asJSON bool
	)
	cmd := &cobra.Command{
		Use:   "list <type>",
		Short: "List data points for a data type (e.g. heart-rate, sleep, steps)",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			return app.runDataList(cmd, args[0], date, days, from, to, all)
		},
	}
	cmd.Flags().StringVar(&date, "date", "today", "civil window anchor: today | yesterday | YYYY-MM-DD")
	cmd.Flags().IntVar(&days, "days", 7, "number of days back from --date to include")
	cmd.Flags().StringVar(&from, "from", "", "explicit window start (RFC3339); overrides --date/--days")
	cmd.Flags().StringVar(&to, "to", "", "explicit window end (RFC3339); overrides --date/--days")
	cmd.Flags().BoolVar(&all, "all", false, "ignore the time window and list everything for the type")
	// Output is always a JSON array of raw data points; --json is accepted for
	// consistency with the other commands but is a no-op.
	cmd.Flags().BoolVar(&asJSON, "json", true, "machine-readable output (always on for data list)")
	return cmd
}

func (a *App) runDataList(cmd *cobra.Command, typeName, date string, days int, from, to string, all bool) error {
	dt, ok := api.LookupDataType(typeName)
	if !ok {
		return withCode(ExitUsage, fmt.Errorf(
			"unknown data type %q; run `google-health-cli types list` to see all %d types", typeName, len(api.DataTypes()),
		))
	}
	if !dt.Supports("list") {
		return withCode(ExitUsage, fmt.Errorf(
			"data type %q does not support list (supported: %v); it is a rollup/reconcile-only type",
			dt.EndpointName, dt.Operations,
		))
	}

	start, end, filtered, err := resolveWindow(date, days, from, to, all)
	if err != nil {
		return withCode(ExitUsage, err)
	}

	client, _, err := a.apiClient(cmd.Context())
	if err != nil {
		return err
	}
	points, err := client.ListDataPoints(cmd.Context(), dt, start, end, filtered)
	if err != nil {
		if filtered && strings.Contains(err.Error(), "DATA_POINT_FILTER") {
			return withCode(ExitAuth, fmt.Errorf(
				"%w\nhint: %q may not support server-side time filtering — re-run with --all and filter client-side",
				err, dt.EndpointName,
			))
		}
		return withCode(ExitAuth, err)
	}

	raws := make([]json.RawMessage, 0, len(points))
	for _, p := range points {
		raws = append(raws, p.Raw)
	}
	emitPrivacyNotice(cmd.ErrOrStderr())
	if err := writeJSON(cmd.OutOrStdout(), raws); err != nil {
		return err
	}
	fprintf(cmd.ErrOrStderr(), "%d %s data point(s)\n", len(raws), dt.EndpointName)
	return nil
}

// resolveWindow turns the window flags into a [start, end) range and whether a
// time filter should be applied. --all wins (no filter); otherwise an explicit
// --from/--to pair wins over the civil --date/--days window.
func resolveWindow(date string, days int, from, to string, all bool) (start, end time.Time, filtered bool, err error) {
	if all {
		return time.Time{}, time.Time{}, false, nil
	}
	if from != "" || to != "" {
		if from == "" || to == "" {
			return time.Time{}, time.Time{}, false, fmt.Errorf("--from and --to must be given together")
		}
		start, err = time.Parse(time.RFC3339, from)
		if err != nil {
			return time.Time{}, time.Time{}, false, fmt.Errorf("invalid --from %q (want RFC3339)", from)
		}
		end, err = time.Parse(time.RFC3339, to)
		if err != nil {
			return time.Time{}, time.Time{}, false, fmt.Errorf("invalid --to %q (want RFC3339)", to)
		}
		return start, end, true, nil
	}
	target, err := resolveDate(date)
	if err != nil {
		return time.Time{}, time.Time{}, false, err
	}
	start, end = window(target, days)
	return start, end, true, nil
}
