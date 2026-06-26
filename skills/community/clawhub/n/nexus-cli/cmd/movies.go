package cmd

import (
	"fmt"
	"sort"

	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var moviesCmd = &cobra.Command{
	Use:   "movies",
	Short: "List all movies in Radarr",
	Long: `List all movies in Radarr with file status and size.

Fetches the full movie list from Radarr and displays each with:
  - File status: filled circle (on disk) or empty circle (missing)
  - Title and year
  - File size on disk

API endpoints used:
  Radarr   GET /api/v3/movie`,
	Example: "  admirarr movies",
	Run:     runMovies,
}

func init() {
	rootCmd.AddCommand(moviesCmd)
}

func runMovies(cmd *cobra.Command, args []string) {
	data, err := arr.New("radarr").Movies()
	if err != nil {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": "Cannot reach Radarr"})
		} else {
			ui.PrintBanner()
			fmt.Println(ui.Bold("\n  Radarr — Movies\n"))
			fmt.Printf("  %s\n", ui.Err("Cannot reach Radarr"))
		}
		return
	}
	if len(data) == 0 {
		if ui.IsJSON() {
			ui.PrintJSON([]struct{}{})
		} else {
			ui.PrintBanner()
			fmt.Println(ui.Bold("\n  Radarr — Movies\n"))
			fmt.Printf("  %s\n", ui.Dim("No movies added"))
		}
		return
	}

	sort.Slice(data, func(i, j int) bool { return data[i].Title < data[j].Title })

	type movieOut struct {
		Title      string `json:"title"`
		Year       int    `json:"year"`
		HasFile    bool   `json:"has_file"`
		SizeOnDisk int64  `json:"size_on_disk"`
	}
	var out []movieOut
	for _, m := range data {
		out = append(out, movieOut{Title: m.Title, Year: m.Year, HasFile: m.HasFile, SizeOnDisk: m.SizeOnDisk})
	}

	ui.PrintOrJSON(out, func() {
		ui.PrintBanner()
		fmt.Println(ui.Bold("\n  Radarr — Movies\n"))
		for _, m := range data {
			status := ui.Err("○")
			size := ""
			if m.HasFile {
				status = ui.Ok("●")
				size = ui.FmtSize(m.SizeOnDisk)
			}
			fmt.Printf("  %s %s (%d) %s\n", status, m.Title, m.Year, ui.Dim(size))
		}
		fmt.Printf("\n  %s\n\n", ui.Dim(fmt.Sprintf("%d movies total", len(data))))
	})
}
