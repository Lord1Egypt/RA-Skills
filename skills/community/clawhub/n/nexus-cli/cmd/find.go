package cmd

import (
	"fmt"
	"strings"

	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var findCmd = &cobra.Command{
	Use:   "find <query>",
	Short: "Search Radarr releases for a movie",
	Long: `Search Radarr releases for a specific movie.

Looks up a movie in Radarr by title, then searches for available releases.
Shows quality, size, seeders, and rejection status.

API endpoints used:
  Radarr   GET /api/v3/movie
  Radarr   GET /api/v3/release?movieId=<id>`,
	Example: "  admirarr find dune\n  admirarr find \"blade runner 2049\"",
	Args:    cobra.MinimumNArgs(1),
	Run:     runFind,
}

func init() {
	rootCmd.AddCommand(findCmd)
}

func runFind(cmd *cobra.Command, args []string) {
	query := strings.ToLower(strings.Join(args, " "))

	client := arr.New("radarr")
	movies, err := client.Movies()
	if err != nil {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": "Cannot reach Radarr"})
		} else {
			ui.PrintBanner()
			fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  Radarr Interactive Search: %s\n", query)))
			fmt.Printf("  %s\n", ui.Err("Cannot reach Radarr"))
		}
		return
	}

	var match *arr.Movie
	for i, m := range movies {
		if strings.Contains(strings.ToLower(m.Title), query) {
			match = &movies[i]
			break
		}
	}
	if match == nil {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": fmt.Sprintf("Movie not found in Radarr: %s", query)})
		} else {
			ui.PrintBanner()
			fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  Radarr Interactive Search: %s\n", query)))
			fmt.Printf("  %s\n", ui.Err(fmt.Sprintf("Movie not found in Radarr: %s", query)))
		}
		return
	}

	releases, err := client.Releases(match.ID)
	if err != nil || len(releases) == 0 {
		if ui.IsJSON() {
			ui.PrintJSON([]struct{}{})
		} else {
			ui.PrintBanner()
			fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  Radarr Interactive Search: %s\n", query)))
			fmt.Printf("  Searching releases for: %s (ID: %d)\n", ui.Bold(match.Title), match.ID)
			fmt.Printf("  %s\n", ui.Err("No releases found"))
		}
		return
	}

	type releaseOut struct {
		Title    string `json:"title"`
		Quality  string `json:"quality"`
		Size     int64  `json:"size"`
		Seeders  int    `json:"seeders"`
		Rejected bool   `json:"rejected"`
	}
	var out []releaseOut
	for _, r := range releases {
		out = append(out, releaseOut{
			Title: r.Title, Quality: r.Quality.Quality.Name,
			Size: r.Size, Seeders: r.Seeders, Rejected: r.Rejected,
		})
	}

	ui.PrintOrJSON(out, func() {
		ui.PrintBanner()
		fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  Radarr Interactive Search: %s\n", query)))
		fmt.Printf("  Searching releases for: %s (ID: %d)\n", ui.Bold(match.Title), match.ID)
		limit := 10
		if len(releases) < limit {
			limit = len(releases)
		}
		for i, r := range releases[:limit] {
			title := r.Title
			if len(title) > 65 {
				title = title[:65]
			}
			status := ui.Ok("OK")
			if r.Rejected {
				status = ui.Err("REJECTED")
			}
			quality := r.Quality.Quality.Name
			size := ui.FmtSize(r.Size)
			fmt.Printf("  %s %s %s\n", ui.Dim(fmt.Sprintf("%2d.", i+1)), status, title)
			fmt.Printf("      %s | %s | Seeds: %d\n", quality, size, r.Seeders)
			if r.Rejected && len(r.Rejections) > 0 {
				for j, rej := range r.Rejections {
					if j >= 2 {
						break
					}
					fmt.Printf("      %s\n", ui.Warn(rej))
				}
			}
		}
		fmt.Println()
	})
}
