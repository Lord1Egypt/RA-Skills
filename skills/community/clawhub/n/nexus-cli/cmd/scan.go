package cmd

import (
	"fmt"

	"github.com/maxtechera/admirarr/internal/media"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var scanCmd = &cobra.Command{
	Use:   "scan",
	Short: "Trigger media server library scan",
	Long: `Trigger a library scan on your media server (Jellyfin or Plex).

Auto-detects which media server is running and triggers a scan.

API endpoints used:
  Jellyfin   POST /Library/Refresh
  Plex       GET  /library/sections + POST /library/sections/{key}/refresh`,
	Example: "  admirarr scan",
	Run:     runScan,
}

func init() {
	rootCmd.AddCommand(scanCmd)
}

func runScan(cmd *cobra.Command, args []string) {
	server := media.Detect()
	if server == nil {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"status": "error", "message": "No media server found (Jellyfin or Plex)"})
		} else {
			ui.PrintBanner()
			fmt.Printf("  %s\n", ui.Err("No media server found (Jellyfin or Plex)"))
		}
		return
	}

	results, err := server.LibraryScan()
	if err != nil && len(results) == 0 {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"status": "error", "message": fmt.Sprintf("Failed: %v", err)})
		} else {
			ui.PrintBanner()
			fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  Triggering %s Library Scan...\n", server.Name())))
			fmt.Printf("  %s\n", ui.Err(fmt.Sprintf("Failed: %v", err)))
		}
		return
	}

	if ui.IsJSON() {
		ui.PrintJSON(map[string]string{"status": "ok", "message": "Library scan triggered"})
	} else {
		ui.PrintBanner()
		fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  Triggering %s Library Scan...\n", server.Name())))
		for _, r := range results {
			if r.OK {
				fmt.Printf("  %s Library scan triggered: %s\n", ui.Ok("●"), r.Library)
			} else {
				fmt.Printf("  %s Scan failed for %s: %v\n", ui.Err("●"), r.Library, r.Err)
			}
		}
		fmt.Println()
	}
}
