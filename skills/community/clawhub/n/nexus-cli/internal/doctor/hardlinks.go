package doctor

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"syscall"

	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/qbit"
	"github.com/maxtechera/admirarr/internal/ui"
)

// checkHardlinks validates TRaSH Guides directory structure and filesystem layout
// for proper hardlink support.
func checkHardlinks(r *Result) {
	fmt.Println(ui.Bold("\n  Hardlinks & Directory Structure"))
	fmt.Println(ui.Separator())

	dataPath := config.DataPath()
	if dataPath == "" {
		fmt.Printf("  %s %s\n", ui.Dim("—"), ui.Dim("data_path not configured (skipping)"))
		return
	}

	// 1. Check TRaSH Guides directory structure
	expectedDirs := []string{
		"torrents", "torrents/movies", "torrents/tv",
		"media", "media/movies", "media/tv",
	}

	presentDirs := 0
	missingDirs := []string{}
	for _, dir := range expectedDirs {
		full := filepath.Join(dataPath, dir)
		if info, err := os.Stat(full); err == nil && info.IsDir() {
			presentDirs++
		} else {
			missingDirs = append(missingDirs, dir)
		}
	}

	if presentDirs == len(expectedDirs) {
		r.ChecksPassed++
		fmt.Printf("  %s TRaSH directory structure: %s\n", ui.Ok("✓"), ui.Ok("complete"))
	} else if presentDirs > 0 {
		fmt.Printf("  %s TRaSH directory structure: %s missing: %s\n",
			ui.Warn("!"), ui.Warn("partial"),
			strings.Join(missingDirs, ", "))
		r.Issues = append(r.Issues, Issue{Description:
			fmt.Sprintf("DIRECTORY STRUCTURE: Missing TRaSH Guides directories under %s: %s. "+
				"See https://trash-guides.info/Hardlinks/How-to-setup-for/Docker/",
				dataPath, strings.Join(missingDirs, ", ")),
		})
	} else {
		fmt.Printf("  %s TRaSH directory structure: %s at %s\n",
			ui.Err("✗"), ui.Err("not found"), dataPath)
		r.Issues = append(r.Issues, Issue{Description:
			fmt.Sprintf("DIRECTORY STRUCTURE: No TRaSH Guides directories found under %s. "+
				"See https://trash-guides.info/Hardlinks/How-to-setup-for/Docker/", dataPath),
		})
	}

	// 2. Check same filesystem (torrents and media must be on same device for hardlinks)
	torrentsPath := filepath.Join(dataPath, "torrents")
	mediaPath := filepath.Join(dataPath, "media")

	torrentsStat, err1 := os.Stat(torrentsPath)
	mediaStat, err2 := os.Stat(mediaPath)

	if err1 == nil && err2 == nil {
		var tDev, mDev uint64
		if sys, ok := torrentsStat.Sys().(*syscall.Stat_t); ok {
			tDev = sys.Dev
		}
		if sys, ok := mediaStat.Sys().(*syscall.Stat_t); ok {
			mDev = sys.Dev
		}

		if tDev != 0 && mDev != 0 {
			if tDev == mDev {
				r.ChecksPassed++
				fmt.Printf("  %s Same filesystem: torrents + media (hardlinks possible)\n", ui.Ok("✓"))
			} else {
				r.Issues = append(r.Issues, Issue{Description:
					fmt.Sprintf("CROSS-FILESYSTEM: %s and %s are on different devices. "+
						"Hardlinks won't work — Sonarr/Radarr will copy instead of link. "+
						"Mount both under the same volume.", torrentsPath, mediaPath),
				})
				fmt.Printf("  %s %s\n", ui.Err("✗"), ui.Err("torrents and media on different filesystems (hardlinks impossible)"))
			}
		}
	} else {
		fmt.Printf("  %s Same filesystem check: %s\n", ui.Dim("—"), ui.Dim("directories not accessible"))
	}

	// 3. Check qBittorrent save path alignment
	if config.IsConfigured("qbittorrent") {
		qc := qbit.New()
		prefs, err := qc.Preferences()
		if err == nil && prefs.SavePath != "" {
			if strings.HasPrefix(prefs.SavePath, "/data/torrents") ||
				strings.HasPrefix(prefs.SavePath, filepath.Join(dataPath, "torrents")) {
				r.ChecksPassed++
				fmt.Printf("  %s qBittorrent save path: %s (inside data/torrents)\n", ui.Ok("✓"), prefs.SavePath)
			} else {
				r.Issues = append(r.Issues, Issue{Description:
					fmt.Sprintf("QBIT SAVE PATH: qBittorrent save path is %s — expected under /data/torrents for TRaSH Guides hardlink structure. "+
						"Update in qBittorrent Options → Downloads → Default Save Path.", prefs.SavePath),
				})
				fmt.Printf("  %s qBittorrent save path: %s %s\n",
					ui.Warn("!"), prefs.SavePath, ui.Warn("(not under /data/torrents)"))
			}
		}
	}
}
