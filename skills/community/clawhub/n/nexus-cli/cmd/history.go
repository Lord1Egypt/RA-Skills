package cmd

import (
	"fmt"

	"github.com/maxtechera/admirarr/internal/media"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var historyCmd = &cobra.Command{
	Use:   "history",
	Short: "Watch history from media server",
	Long: `Show watch history from your media server (Jellyfin or Plex).

Auto-detects which media server is running and fetches watch history.
Uses Tautulli if configured and reachable, otherwise falls back to
the media server's built-in activity log.

API endpoints used:
  Tautulli   GET /api/v2?cmd=get_history&length=10
  Jellyfin   GET /System/ActivityLog/Entries
  Plex       Requires Tautulli`,
	Example: "  admirarr history",
	Run:     runHistory,
}

func init() {
	rootCmd.AddCommand(historyCmd)
}

func runHistory(cmd *cobra.Command, args []string) {
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

	history, err := server.WatchHistory(10)
	if err != nil {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": fmt.Sprintf("Failed: %v", err)})
		} else {
			ui.PrintBanner()
			fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  %s — Watch History\n", server.Name())))
			fmt.Printf("  %s\n", ui.Err(fmt.Sprintf("Failed: %v", err)))
		}
		return
	}

	type historyOut struct {
		Title   string `json:"title"`
		User    string `json:"user"`
		Minutes int    `json:"minutes"`
	}
	var out []historyOut
	for _, h := range history {
		out = append(out, historyOut{Title: h.Title, User: h.User, Minutes: h.Minutes})
	}

	ui.PrintOrJSON(out, func() {
		ui.PrintBanner()
		fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  %s — Watch History\n", server.Name())))
		if len(history) == 0 {
			fmt.Printf("  %s\n", ui.Dim("No watch history yet"))
			return
		}
		for _, h := range history {
			if h.User != "" {
				fmt.Printf("  %15s  %s %s\n", ui.GoldText(h.User), h.Title, ui.Dim(fmt.Sprintf("(%d min)", h.Minutes)))
			} else {
				name := h.Title
				if len(name) > 60 {
					name = name[:60] + "..."
				}
				fmt.Printf("  %s\n", name)
			}
		}
		fmt.Println()
	})
}
