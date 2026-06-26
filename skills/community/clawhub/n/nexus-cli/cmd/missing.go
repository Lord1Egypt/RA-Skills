package cmd

import (
	"fmt"

	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var missingCmd = &cobra.Command{
	Use:   "missing",
	Short: "Monitored content without files",
	Long: `Show monitored content that is missing files.

Movies: from Radarr, filtered by monitored=true and hasFile=false.
Episodes: from Sonarr wanted/missing endpoint, sorted by air date.

API endpoints used:
  Radarr   GET /api/v3/movie
  Sonarr   GET /api/v3/wanted/missing?pageSize=20`,
	Example: "  admirarr missing",
	Run:     runMissing,
}

func init() {
	rootCmd.AddCommand(missingCmd)
}

func runMissing(cmd *cobra.Command, args []string) {
	type missingMovieOut struct {
		Title  string `json:"title"`
		Year   int    `json:"year"`
		Status string `json:"status"`
	}
	type missingEpisodeOut struct {
		Series  string `json:"series"`
		Season  int    `json:"season"`
		Episode int    `json:"episode"`
		Title   string `json:"title"`
	}
	type missingOut struct {
		Movies   []missingMovieOut   `json:"movies"`
		Episodes []missingEpisodeOut `json:"episodes"`
	}

	out := missingOut{Movies: []missingMovieOut{}, Episodes: []missingEpisodeOut{}}

	// Movies
	movies, moviesErr := arr.New("radarr").Movies()
	if moviesErr == nil {
		for _, m := range movies {
			if m.Monitored && !m.HasFile {
				out.Movies = append(out.Movies, missingMovieOut{Title: m.Title, Year: m.Year, Status: m.Status})
			}
		}
	}

	// Episodes
	eps, epsErr := arr.New("sonarr").WantedMissing(20, map[string]string{
		"sortKey":       "airDateUtc",
		"sortDirection": "descending",
	})

	if epsErr == nil {
		for _, e := range eps.Records {
			out.Episodes = append(out.Episodes, missingEpisodeOut{
				Series: e.Series.Title, Season: e.SeasonNumber, Episode: e.EpisodeNumber, Title: e.Title,
			})
		}
	}

	ui.PrintOrJSON(out, func() {
		ui.PrintBanner()
		fmt.Println(ui.Bold("\n  Missing Content\n"))

		if moviesErr == nil {
			fmt.Println(ui.Bold(fmt.Sprintf("  Movies (%d missing)", len(out.Movies))))
			for _, m := range out.Movies {
				fmt.Printf("  %s %s (%d) — %s\n", ui.Err("○"), m.Title, m.Year, m.Status)
			}
		} else {
			fmt.Printf("  %s\n", ui.Err("Cannot reach Radarr"))
		}

		fmt.Println()
		if epsErr == nil {
			fmt.Println(ui.Bold(fmt.Sprintf("  Episodes (%d missing)", eps.TotalRecords)))
			limit := 15
			if len(eps.Records) < limit {
				limit = len(eps.Records)
			}
			for _, e := range eps.Records[:limit] {
				fmt.Printf("  %s %s S%02dE%02d — %s\n", ui.Err("○"), e.Series.Title, e.SeasonNumber, e.EpisodeNumber, e.Title)
			}
		} else {
			fmt.Printf("  %s\n", ui.Err("Cannot reach Sonarr"))
		}
		fmt.Println()
	})
}
