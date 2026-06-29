package cli

import (
	"fmt"

	"github.com/spf13/cobra"

	"github.com/stozo04/google-health-cli/internal/api"
)

// newRollupCmd is the server-side aggregation surface: `rollup daily <type>`
// returns the Google Health API's daily rollup rows (e.g. a steps total per
// civil day) instead of the raw per-minute points `data list` returns. It is the
// only way to read the rollup-only types (active-minutes, total-calories, …).
// Read-only: dailyRollUp is a POST verb but a pure query, not a mutation.
func newRollupCmd(app *App) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "rollup",
		Short: "Read server-aggregated rollups for a data type",
		Args:  cobra.NoArgs,
		RunE: func(c *cobra.Command, _ []string) error {
			return c.Help()
		},
	}
	cmd.AddCommand(newRollupDailyCmd(app))
	return cmd
}

// newRollupDailyCmd rolls one data type up to per-civil-day aggregates over a
// time window, emitting the raw API JSON array on stdout (the verbatim rollup
// rows). A one-line count goes to stderr. Window flags mirror `data list`,
// minus --all: the dailyRollUp request requires a bounded range.
func newRollupDailyCmd(app *App) *cobra.Command {
	var (
		date   string
		days   int
		from   string
		to     string
		asJSON bool
	)
	cmd := &cobra.Command{
		Use:   "daily <type>",
		Short: "Daily server-side rollup totals for a data type (e.g. steps, active-minutes)",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			return app.runRollupDaily(cmd, args[0], date, days, from, to)
		},
	}
	cmd.Flags().StringVar(&date, "date", "today", "civil window anchor: today | yesterday | YYYY-MM-DD")
	cmd.Flags().IntVar(&days, "days", 7, "number of days back from --date to include")
	cmd.Flags().StringVar(&from, "from", "", "explicit window start (RFC3339); overrides --date/--days")
	cmd.Flags().StringVar(&to, "to", "", "explicit window end (RFC3339); overrides --date/--days")
	// Output is always a JSON array of raw rollup rows; --json is accepted for
	// consistency with the other commands but is a no-op.
	cmd.Flags().BoolVar(&asJSON, "json", true, "machine-readable output (always on for rollup)")
	return cmd
}

func (a *App) runRollupDaily(cmd *cobra.Command, typeName, date string, days int, from, to string) error {
	dt, ok := api.LookupDataType(typeName)
	if !ok {
		return withCode(ExitUsage, fmt.Errorf(
			"unknown data type %q; run `google-health-cli types list` to see all %d types", typeName, len(api.DataTypes()),
		))
	}
	if !dt.Supports("dailyRollUp") {
		return withCode(ExitUsage, fmt.Errorf(
			"data type %q does not support dailyRollUp (supported: %v); run `google-health-cli data list %s` instead",
			dt.EndpointName, dt.Operations, dt.EndpointName,
		))
	}

	// --all is intentionally absent: dailyRollUp requires a bounded civil range.
	start, end, _, err := resolveWindow(date, days, from, to, false)
	if err != nil {
		return withCode(ExitUsage, err)
	}

	client, _, err := a.apiClient(cmd.Context())
	if err != nil {
		return err
	}
	points, err := client.RollUpDaily(cmd.Context(), dt, start, end)
	if err != nil {
		return withCode(ExitAuth, err)
	}

	emitPrivacyNotice(cmd.ErrOrStderr())
	if err := writeJSON(cmd.OutOrStdout(), points); err != nil {
		return err
	}
	fprintf(cmd.ErrOrStderr(), "%d %s daily rollup(s)\n", len(points), dt.EndpointName)
	return nil
}
