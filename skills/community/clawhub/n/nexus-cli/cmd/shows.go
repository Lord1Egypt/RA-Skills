package cmd

import (
	"fmt"
	"sort"

	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var showsCmd = &cobra.Command{
	Use:   "shows",
	Short: "List all TV shows in Sonarr",
	Long: `List all TV shows in Sonarr with episode counts and size.

Fetches the full series list from Sonarr and displays each with:
  - Episode count: episodes on disk / total episodes
  - Color-coded: green (complete), yellow (partial), red (none)
  - Title, year, and size on disk

API endpoints used:
  Sonarr   GET /api/v3/series`,
	Example: "  admirarr shows",
	Run:     runShows,
}

func init() {
	rootCmd.AddCommand(showsCmd)
}

func runShows(cmd *cobra.Command, args []string) {
	data, err := arr.New("sonarr").Series()
	if err != nil {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": "Cannot reach Sonarr"})
		} else {
			ui.PrintBanner()
			fmt.Println(ui.Bold("\n  Sonarr — TV Shows\n"))
			fmt.Printf("  %s\n", ui.Err("Cannot reach Sonarr"))
		}
		return
	}
	if len(data) == 0 {
		if ui.IsJSON() {
			ui.PrintJSON([]struct{}{})
		} else {
			ui.PrintBanner()
			fmt.Println(ui.Bold("\n  Sonarr — TV Shows\n"))
			fmt.Printf("  %s\n", ui.Dim("No shows added"))
		}
		return
	}

	sort.Slice(data, func(i, j int) bool { return data[i].Title < data[j].Title })

	type showOut struct {
		Title        string `json:"title"`
		Year         int    `json:"year"`
		Episodes     int    `json:"episodes"`
		EpisodeFiles int    `json:"episode_files"`
		SizeOnDisk   int64  `json:"size_on_disk"`
	}
	var out []showOut
	for _, s := range data {
		out = append(out, showOut{
			Title: s.Title, Year: s.Year,
			Episodes: s.Statistics.EpisodeCount, EpisodeFiles: s.Statistics.EpisodeFileCount,
			SizeOnDisk: s.Statistics.SizeOnDisk,
		})
	}

	ui.PrintOrJSON(out, func() {
		ui.PrintBanner()
		fmt.Println(ui.Bold("\n  Sonarr — TV Shows\n"))
		for _, s := range data {
			have := s.Statistics.EpisodeFileCount
			total := s.Statistics.EpisodeCount
			pct := fmt.Sprintf("%d/%d", have, total)
			colorFn := ui.Err
			if have == total && total > 0 {
				colorFn = ui.Ok
			} else if have > 0 {
				colorFn = ui.Warn
			}
			size := ui.FmtSize(s.Statistics.SizeOnDisk)
			fmt.Printf("  %12s  %s (%d) %s\n", colorFn(pct), s.Title, s.Year, ui.Dim(size))
		}
		fmt.Printf("\n  %s\n\n", ui.Dim(fmt.Sprintf("%d shows total", len(data))))
	})
}
