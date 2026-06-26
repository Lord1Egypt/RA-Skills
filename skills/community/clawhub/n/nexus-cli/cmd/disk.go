package cmd

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/qbit"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var diskCmd = &cobra.Command{
	Use:   "disk",
	Short: "Disk space breakdown",
	Long: `Show disk space breakdown for media directories.

Discovers paths by querying service APIs:
  - Radarr/Sonarr root folders for media paths
  - qBittorrent preferences for torrent download path
Falls back to the configured data_path if no services respond.`,
	Example: "  admirarr disk",
	Run:     runDisk,
}

func init() {
	rootCmd.AddCommand(diskCmd)
}

type diskPath struct {
	path  string
	label string
}

// discoverPaths queries Radarr, Sonarr, and qBittorrent APIs to find actual
// media and download directories. Falls back to config data_path if no
// services are reachable.
func discoverPaths() []diskPath {
	seen := make(map[string]bool)
	var paths []diskPath

	add := func(p, label string) {
		if p == "" || seen[p] {
			return
		}
		seen[p] = true
		paths = append(paths, diskPath{path: p, label: label})
	}

	// Always include the base data path first.
	dataPath := config.DataPath()
	add(dataPath, dataPath)

	apiDiscovered := false

	// Query Radarr root folders.
	if api.CheckReachable("radarr") {
		folders, err := arr.New("radarr").RootFolders()
		if err == nil {
			for _, f := range folders {
				add(f.Path, fmt.Sprintf("radarr: %s", f.Path))
				apiDiscovered = true
			}
		}
	}

	// Query Sonarr root folders.
	if api.CheckReachable("sonarr") {
		folders, err := arr.New("sonarr").RootFolders()
		if err == nil {
			for _, f := range folders {
				add(f.Path, fmt.Sprintf("sonarr: %s", f.Path))
				apiDiscovered = true
			}
		}
	}

	// Query qBittorrent save path.
	if api.CheckReachable("qbittorrent") {
		prefs, err := qbit.New().Preferences()
		if err == nil && prefs.SavePath != "" {
			add(prefs.SavePath, fmt.Sprintf("qbittorrent: %s", prefs.SavePath))
			apiDiscovered = true
		}
	}

	// Fallback: if no services responded, use TRaSH Guides defaults.
	if !apiDiscovered {
		add(filepath.Join(dataPath, "torrents"), "torrents")
		add(filepath.Join(dataPath, "media", "movies"), "media/movies")
		add(filepath.Join(dataPath, "media", "tv"), "media/tv")
	}

	return paths
}

func runDisk(cmd *cobra.Command, args []string) {
	paths := discoverPaths()

	type diskOut struct {
		Label      string `json:"label"`
		Path       string `json:"path"`
		UsedBytes  int64  `json:"used_bytes"`
		TotalBytes int64  `json:"total_bytes"`
		Files      int    `json:"files"`
	}
	var out []diskOut

	for _, p := range paths {
		total, free, err := getStatfs(p.path)
		if err != nil {
			out = append(out, diskOut{Label: p.label, Path: p.path, UsedBytes: -1, TotalBytes: -1, Files: 0})
			continue
		}
		used := total - free
		count := 0
		_ = filepath.Walk(p.path, func(_ string, info os.FileInfo, err error) error {
			if err != nil {
				return nil
			}
			if !info.IsDir() {
				count++
			}
			return nil
		})
		out = append(out, diskOut{Label: p.label, Path: p.path, UsedBytes: used, TotalBytes: total, Files: count})
	}

	ui.PrintOrJSON(out, func() {
		ui.PrintBanner()
		fmt.Println(ui.Bold("\n  Disk Space\n"))
		for _, d := range out {
			if d.UsedBytes < 0 {
				fmt.Printf("  %-30s %s\n", d.Label, ui.Err("N/A"))
				continue
			}
			fmt.Printf("  %-30s %10s used / %10s total  (%d files)\n",
				d.Label, ui.FmtSize(d.UsedBytes), ui.FmtSize(d.TotalBytes), d.Files)
		}
		fmt.Println()
	})
}
