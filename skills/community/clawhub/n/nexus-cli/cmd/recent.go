package cmd

import (
	"fmt"

	"github.com/maxtechera/admirarr/internal/media"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var recentCmd = &cobra.Command{
	Use:   "recent",
	Short: "Recently added to media server",
	Long: `Show recently added content in your media server (Jellyfin or Plex).

Auto-detects which media server is running and queries for the 15 most
recently added items.

API endpoints used:
  Jellyfin   GET /Users
  Jellyfin   GET /Users/{UserId}/Items/Latest
  Plex       GET /library/recentlyAdded`,
	Example: "  admirarr recent",
	Run:     runRecent,
}

func init() {
	rootCmd.AddCommand(recentCmd)
}

func runRecent(cmd *cobra.Command, args []string) {
	server := media.Detect()
	if server == nil {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": "No media server found (Jellyfin or Plex)"})
		} else {
			ui.PrintBanner()
			fmt.Printf("  %s\n", ui.Err("No media server found (Jellyfin or Plex)"))
		}
		return
	}

	items, err := server.RecentlyAdded(15)
	if err != nil {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": fmt.Sprintf("Failed: %v", err)})
		} else {
			ui.PrintBanner()
			fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  %s — Recently Added\n", server.Name())))
			fmt.Printf("  %s\n", ui.Err(fmt.Sprintf("Failed: %v", err)))
		}
		return
	}

	type recentOut struct {
		Title string `json:"title"`
		Year  string `json:"year"`
		Type  string `json:"type"`
	}
	var out []recentOut
	for _, item := range items {
		out = append(out, recentOut{Title: item.Title, Year: item.Year, Type: item.Type})
	}

	ui.PrintOrJSON(out, func() {
		ui.PrintBanner()
		fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  %s — Recently Added\n", server.Name())))
		if len(items) == 0 {
			fmt.Printf("  %s\n", ui.Dim("Nothing recently added"))
			return
		}
		for _, item := range items {
			fmt.Printf("  %s %s (%s) — %s\n", ui.Ok("+"), item.Title, item.Year, item.Type)
		}
		fmt.Println()
	})
}
