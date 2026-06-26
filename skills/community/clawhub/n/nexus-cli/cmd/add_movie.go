package cmd

import (
	"fmt"
	"strings"

	"github.com/charmbracelet/huh"
	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var addMovieCmd = &cobra.Command{
	Use:   "add-movie <query>",
	Short: "Search and add a movie to Radarr",
	Long: `Search for a movie and add it to Radarr.

Interactive workflow:
  1. Search Radarr for movies matching the query
  2. Pick from results using an interactive selector
  3. Add to Radarr with default quality profile and trigger search

API endpoints used:
  Radarr   GET  /api/v3/movie/lookup?term=<query>
  Radarr   GET  /api/v3/rootfolder
  Radarr   GET  /api/v3/qualityprofile
  Radarr   POST /api/v3/movie`,
	Example: "  admirarr add-movie interstellar\n  admirarr add-movie \"the godfather\"",
	Args:    cobra.MinimumNArgs(1),
	Run:     runAddMovie,
}

func init() {
	rootCmd.AddCommand(addMovieCmd)
}

func runAddMovie(cmd *cobra.Command, args []string) {
	query := strings.Join(args, " ")
	ui.PrintBanner()
	fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  Search Radarr: %s\n", query)))

	client := arr.New("radarr")

	results, err := client.LookupMovie(query)
	if err != nil || len(results) == 0 {
		fmt.Printf("  %s\n", ui.Err("No results"))
		return
	}

	limit := 5
	if len(results) < limit {
		limit = len(results)
	}
	results = results[:limit]

	// Build options for huh select
	options := make([]huh.Option[int], len(results))
	for i, m := range results {
		title, _ := m["title"].(string)
		year := 0
		if y, ok := m["year"].(float64); ok {
			year = int(y)
		}
		overview, _ := m["overview"].(string)
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
				Title("Pick a movie to add").
				Options(options...).
				Value(&selected),
		),
	)
	if err := form.Run(); err != nil {
		return
	}

	movie := results[selected]

	// Get root folder and quality profile
	roots, err := client.RootFolders()
	if err != nil || len(roots) == 0 {
		fmt.Printf("  %s\n", ui.Err("Cannot get Radarr config"))
		return
	}
	profiles, err := client.QualityProfiles()
	if err != nil || len(profiles) == 0 {
		fmt.Printf("  %s\n", ui.Err("Cannot get Radarr config"))
		return
	}

	movie["qualityProfileId"] = profiles[0].ID
	movie["rootFolderPath"] = roots[0].Path
	movie["monitored"] = true
	movie["addOptions"] = map[string]bool{"searchForMovie": true}

	result, err := client.AddMovie(movie)
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
