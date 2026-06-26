package cmd

import (
	"fmt"
	"strings"

	"github.com/maxtechera/admirarr/internal/qbit"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var downloadsCmd = &cobra.Command{
	Use:   "downloads",
	Short: "Active qBittorrent torrents",
	Long: `Show and manage qBittorrent torrents.

Queries qBittorrent Web API for all torrents and displays:
  - Progress percentage with visual bar
  - Download speed in MB/s
  - Torrent name and size

Subcommands:
  pause    Pause torrents (by hash or "all")
  resume   Resume torrents (by hash or "all")
  remove   Remove torrents (by hash, with optional --delete-files)

API endpoints used:
  qBit   GET  /api/v2/torrents/info
  qBit   POST /api/v2/torrents/pause
  qBit   POST /api/v2/torrents/resume
  qBit   POST /api/v2/torrents/delete
  qBit   GET  /api/v2/app/preferences`,
	Example: `  admirarr downloads
  admirarr downloads pause all
  admirarr downloads resume all
  admirarr downloads remove <hash> --delete-files`,
	Run: runDownloads,
}

var downloadsPauseCmd = &cobra.Command{
	Use:   "pause [hash|all]",
	Short: "Pause torrents",
	Long:  `Pause one or all qBittorrent torrents. Use "all" to pause everything, or pass a torrent hash.`,
	Args:  cobra.ExactArgs(1),
	Run:   runDownloadsPause,
}

var downloadsResumeCmd = &cobra.Command{
	Use:   "resume [hash|all]",
	Short: "Resume torrents",
	Long:  `Resume one or all paused qBittorrent torrents. Use "all" to resume everything, or pass a torrent hash.`,
	Args:  cobra.ExactArgs(1),
	Run:   runDownloadsResume,
}

var downloadsRemoveCmd = &cobra.Command{
	Use:   "remove [hash]",
	Short: "Remove a torrent",
	Long:  `Remove a torrent from qBittorrent. Use --delete-files to also delete downloaded data.`,
	Args:  cobra.ExactArgs(1),
	Run:   runDownloadsRemove,
}

var deleteFiles bool

func init() {
	rootCmd.AddCommand(downloadsCmd)
	downloadsCmd.AddCommand(downloadsPauseCmd)
	downloadsCmd.AddCommand(downloadsResumeCmd)
	downloadsCmd.AddCommand(downloadsRemoveCmd)
	downloadsRemoveCmd.Flags().BoolVar(&deleteFiles, "delete-files", false, "Also delete downloaded files from disk")
}

func runDownloads(cmd *cobra.Command, args []string) {
	data, err := qbit.New().Torrents()
	if err != nil {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": "Cannot reach qBittorrent"})
		} else {
			ui.PrintBanner()
			fmt.Println(ui.Bold("\n  qBittorrent — Downloads\n"))
			fmt.Printf("  %s\n", ui.Err("Cannot reach qBittorrent"))
		}
		return
	}

	type downloadOut struct {
		Hash     string  `json:"hash"`
		Name     string  `json:"name"`
		Size     int64   `json:"size"`
		Progress float64 `json:"progress"`
		Speed    int64   `json:"speed"`
		State    string  `json:"state"`
	}
	var out []downloadOut
	for _, t := range data {
		out = append(out, downloadOut{Hash: t.Hash, Name: t.Name, Size: t.Size, Progress: t.Progress, Speed: t.DLSpeed, State: t.State})
	}

	ui.PrintOrJSON(out, func() {
		ui.PrintBanner()
		fmt.Println(ui.Bold("\n  qBittorrent — Downloads\n"))

		dlStates := map[string]bool{"downloading": true, "stalledDL": true, "forcedDL": true, "metaDL": true}
		seedStates := map[string]bool{"uploading": true, "stalledUP": true, "forcedUP": true}

		var downloading, seeding, paused []int
		for i, t := range data {
			if dlStates[t.State] {
				downloading = append(downloading, i)
			} else if seedStates[t.State] {
				seeding = append(seeding, i)
			} else if strings.Contains(t.State, "paused") {
				paused = append(paused, i)
			}
		}

		if len(downloading) > 0 {
			fmt.Println(ui.Bold("  Active Downloads"))
			for _, i := range downloading {
				t := data[i]
				pct := int(t.Progress * 100)
				speed := float64(t.DLSpeed) / 1048576
				size := ui.FmtSize(t.Size)
				barLen := 15
				filled := barLen * pct / 100
				bar := strings.Repeat("█", filled) + strings.Repeat("░", barLen-filled)
				name := t.Name
				if len(name) > 50 {
					name = name[:50]
				}
				fmt.Printf("  [%s] %s %.1f MB/s  %s %s\n", bar, ui.GoldText(fmt.Sprintf("%d%%", pct)), speed, name, ui.Dim(size))
				fmt.Printf("  %s\n", ui.Dim("  "+t.Hash[:12]+"…"))
			}
		} else {
			fmt.Printf("  %s\n", ui.Dim("No active downloads"))
		}

		if len(seeding) > 0 {
			fmt.Printf("\n  %s", ui.Dim(fmt.Sprintf("%d seeding", len(seeding))))
		}
		if len(paused) > 0 {
			fmt.Printf("  %s", ui.Dim(fmt.Sprintf("%d paused", len(paused))))
		}
		fmt.Printf("  %s\n\n", ui.Dim(fmt.Sprintf("%d total", len(data))))
	})
}

func runDownloadsPause(cmd *cobra.Command, args []string) {
	qc := qbit.New()
	if err := qc.Pause(args[0]); err != nil {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": err.Error()})
		} else {
			fmt.Printf("  %s %s\n", ui.Err("✗"), err)
		}
		return
	}
	if ui.IsJSON() {
		ui.PrintJSON(map[string]string{"status": "paused", "target": args[0]})
	} else {
		fmt.Printf("  %s Paused: %s\n", ui.Ok("✓"), args[0])
	}
}

func runDownloadsResume(cmd *cobra.Command, args []string) {
	qc := qbit.New()
	if err := qc.Resume(args[0]); err != nil {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": err.Error()})
		} else {
			fmt.Printf("  %s %s\n", ui.Err("✗"), err)
		}
		return
	}
	if ui.IsJSON() {
		ui.PrintJSON(map[string]string{"status": "resumed", "target": args[0]})
	} else {
		fmt.Printf("  %s Resumed: %s\n", ui.Ok("✓"), args[0])
	}
}

func runDownloadsRemove(cmd *cobra.Command, args []string) {
	qc := qbit.New()
	if err := qc.Delete(deleteFiles, args[0]); err != nil {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": err.Error()})
		} else {
			fmt.Printf("  %s %s\n", ui.Err("✗"), err)
		}
		return
	}
	action := "Removed"
	if deleteFiles {
		action = "Removed (+ files deleted)"
	}
	if ui.IsJSON() {
		ui.PrintJSON(map[string]string{"status": "removed", "target": args[0], "files_deleted": fmt.Sprintf("%v", deleteFiles)})
	} else {
		fmt.Printf("  %s %s: %s\n", ui.Ok("✓"), action, args[0])
	}
}
