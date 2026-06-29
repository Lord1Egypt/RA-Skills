package cli

import (
	"context"
	"fmt"
	"sort"

	"github.com/spf13/cobra"

	"github.com/stozo04/loseit-cli/internal/config"
	"github.com/stozo04/loseit-cli/internal/export"
	"github.com/stozo04/loseit-cli/internal/nutrition"
)

// newDaysCmd implements `days` — the core emit. It parses the export and prints
// per-day nutrition: a human table by default, or the frozen JSON contract with
// --json (a JSON object keyed by ISO date → nutrition object; empty → {}).
func newDaysCmd(app *App) *cobra.Command {
	var (
		zip    string
		date   string
		days   int
		asJSON bool
	)
	cmd := &cobra.Command{
		Use:   "days",
		Short: "Parse the Lose It export and print per-day nutrition",
		Args:  cobra.NoArgs,
		RunE: func(cmd *cobra.Command, _ []string) error {
			return app.runDays(cmd, zip, date, days, asJSON)
		},
	}
	cmd.Flags().StringVar(&zip, "zip", "", "parse a downloaded export ZIP instead of fetching")
	cmd.Flags().StringVar(&date, "date", "today", "today | yesterday | YYYY-MM-DD")
	cmd.Flags().IntVar(&days, "days", 7, "number of days back to include")
	cmd.Flags().BoolVar(&asJSON, "json", false, "emit the frozen per-day JSON contract")
	return cmd
}

func (a *App) runDays(cmd *cobra.Command, zipPath, date string, days int, asJSON bool) error {
	cfg, err := a.resolveConfig()
	if err != nil {
		return err
	}

	byDay, err := a.loadNutrition(cmd.Context(), cfg, zipPath)
	if err != nil {
		return err
	}

	target, err := resolveDate(date)
	if err != nil {
		return withCode(ExitUsage, err)
	}

	wanted := wantedDates(target, days)
	dates := make([]string, 0, len(byDay))
	for d := range byDay {
		if wanted[d] {
			dates = append(dates, d)
		}
	}
	sort.Strings(dates)

	out := cmd.OutOrStdout()
	if asJSON {
		// A JSON object keyed by ISO date. ISO dates sort lexicographically ==
		// chronologically, and encoding/json sorts map keys, so the object's key
		// order is ascending by date. An empty selection encodes as {}.
		selected := make(map[string]nutrition.Nutrition, len(dates))
		for _, d := range dates {
			selected[d] = byDay[d]
		}
		return writeJSON(out, selected)
	}

	if len(dates) == 0 {
		fprintf(out, "No Lose It entries for the last %d day(s) ending %s.\n",
			days, target.Format("2006-01-02"))
		return nil
	}
	fprintf(out, "Lose It nutrition, last %d day(s) ending %s:\n\n", days, target.Format("2006-01-02"))
	for _, d := range dates {
		n := byDay[d]
		fprintf(out, "  %s: %d cal, %dg protein, %dg fiber, %dg carb, %dg fat  (%d meals)\n",
			d, n.CaloriesFood, n.ProteinG, n.FiberG, n.CarbsG, n.FatG, len(n.Meals))
	}
	return nil
}

// loadNutrition obtains the export ZIP (via --zip or the cookie fetch), reads
// its CSVs, and aggregates per-day nutrition. Every failure on this path is an
// export/parse failure → exit 2.
func (a *App) loadNutrition(ctx context.Context, cfg *config.Config, zipPath string) (map[string]nutrition.Nutrition, error) {
	data, err := export.LoadZipBytes(ctx, cfg, zipPath)
	if err != nil {
		return nil, withCode(ExitExport, err)
	}
	food, err := export.ReadCSV(data, export.FoodLogsCSV)
	if err != nil {
		return nil, withCode(ExitExport, err)
	}
	summary, err := export.ReadCSV(data, export.SummaryCSV)
	if err != nil {
		return nil, withCode(ExitExport, err)
	}
	if len(food) == 0 {
		return nil, withCode(ExitExport, fmt.Errorf("%s not found / empty in the export", export.FoodLogsCSV))
	}
	return nutrition.BuildByDay(food, summary), nil
}
