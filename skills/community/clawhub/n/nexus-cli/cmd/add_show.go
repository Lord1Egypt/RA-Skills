package cmd

import (
	"fmt"
	"strings"

	"github.com/charmbracelet/huh"
	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var addShowCmd = &cobra.Command{
	Use:   "add-show <query>",
	Short: "Search and add a TV show to Sonarr",
	Long: `Search for a TV show and add it to Sonarr.

Interactive workflow:
  1. Search Sonarr for series matching the query
  2. Pick from results using an interactive selector
  3. Add to Sonarr with default quality profile and trigger search

API endpoints used:
  Sonarr   GET  /api/v3/series/lookup?term=<query>
  Sonarr   GET  /api/v3/rootfolder
  Sonarr   GET  /api/v3/qualityprofile
  Sonarr   POST /api/v3/series`,
	Example: "  admirarr add-show \"the bear\"\n  admirarr add-show severance",
	Args:    cobra.MinimumNArgs(1),
	Run:     runAddShow,
}

func init() {
	rootCmd.AddCommand(addShowCmd)
}

func runAddShow(cmd *cobra.Command, args []string) {
	query := strings.Join(args, " ")
	ui.PrintBanner()
	fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  Search Sonarr: %s\n", query)))

	client := arr.New("sonarr")

	results, err := client.LookupSeries(query)
	if err != nil || len(results) == 0 {
		fmt.Printf("  %s\n", ui.Err("No results"))
		return
	}

	limit := 5
	if len(results) < limit {
		limit = len(results)
	}
	results = results[:limit]

	options := make([]huh.Option[int], len(results))
	for i, s := range results {
		title, _ := s["title"].(string)
		year := 0
		if y, ok := s["year"].(float64); ok {
			year = int(y)
		}
		overview, _ := s["overview"].(string)
		if len(overview) > 80 {
			overview = overview[:80]
		}
		label := fmt.Sprintf("%s (%d)", title, year)
		if overview != "" {
			label += "\n     " + ui.Dim(overview)
		}
		options[i] = huh.NewOption(label, i)
	}

	var selected int
	form := huh.NewForm(
		huh.NewGroup(
			huh.NewSelect[int]().
				Title("Pick a show to add").
				Options(options...).
				Value(&selected),
		),
	)
	if err := form.Run(); err != nil {
		return
	}

	series := results[selected]

	roots, err := client.RootFolders()
	if err != nil || len(roots) == 0 {
		fmt.Printf("  %s\n", ui.Err("Cannot get Sonarr config"))
		return
	}
	profiles, err := client.QualityProfiles()
	if err != nil || len(profiles) == 0 {
		fmt.Printf("  %s\n", ui.Err("Cannot get Sonarr config"))
		return
	}

	series["qualityProfileId"] = profiles[0].ID
	series["rootFolderPath"] = roots[0].Path
	series["monitored"] = true
	series["addOptions"] = map[string]interface{}{
		"searchForMissingEpisodes": true,
		"monitor":                  "all",
	}

	result, err := client.AddSeries(series)
	if err != nil {
		fmt.Printf("\n  %s\n\n", ui.Err("Failed to add."))
		return
	}

	if _, ok := result["id"]; ok {
		title, _ := result["title"].(string)
		year := 0
		if y, ok := result["year"].(float64); ok {
			year = int(y)
		}
		fmt.Printf("\n  %s %s (%d) — searching...\n\n", ui.Ok("Added:"), title, year)
		return
	}
	fmt.Printf("\n  %s\n\n", ui.Err("Failed to add."))
}
