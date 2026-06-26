package setup

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/ui"
)

// arrRootFolders maps *Arr services to their expected root folder subdirectories.
var arrRootFolders = []struct {
	service string
	subdir  string
}{
	{"radarr", "media/movies"},
	{"sonarr", "media/tv"},
	{"lidarr", "media/music"},
	{"readarr", "media/books"},
	{"whisparr", "media/xxx"},
}

// ValidateRootFolders runs Phase 6: root folder and media path validation.
func ValidateRootFolders(state *SetupState) StepResult {
	r := StepResult{Name: "Root Folders"}

	dataPath := state.DataPath
	if dataPath == "" {
		dataPath = config.DataPath()
	}

	// 6a. Create missing media directories (TRaSH Guides structure)
	fmt.Println(ui.Bold("  Media Directories"))

	// Build directory list based on selected services
	requiredDirs := []string{
		"media", "torrents",
	}
	for _, dc := range arrDownloadConfig {
		if state.Services[dc.Service] != nil {
			requiredDirs = append(requiredDirs, dc.TorrentDir)
		}
	}
	for _, ac := range arrRootFolders {
		if state.Services[ac.service] != nil {
			requiredDirs = append(requiredDirs, ac.subdir)
		}
	}

	for _, dir := range requiredDirs {
		path := filepath.Join(dataPath, dir)
		if info, err := os.Stat(path); err == nil && info.IsDir() {
			fmt.Printf("  %s %s\n", ui.Ok("✓"), path)
			r.pass()
			continue
		}

		if err := os.MkdirAll(path, 0755); err != nil {
			r.errf("cannot create %s: %v", path, err)
			continue
		}
		fmt.Printf("  %s Created %s\n", ui.Ok("✓"), path)
		r.fix()
	}

	// 6b. Validate root folders in all *Arr services
	fmt.Printf("\n%s\n", ui.Bold("  Root Folders"))

	arrConfigs := arrRootFolders

	for _, ac := range arrConfigs {
		svc := state.Services[ac.service]
		if svc == nil || !svc.Reachable {
			fmt.Printf("  %s %s → %s\n", ui.Dim("—"), titleCase(ac.service), ui.Dim("skipped (not reachable)"))
			r.skip()
			continue
		}

		client := arr.New(ac.service)
		expectedPath := filepath.Join(dataPath, ac.subdir)

		roots, err := client.RootFolders()
		if err != nil {
			r.errf("%s → cannot query root folders: %v", titleCase(ac.service), err)
			continue
		}

		// Check if expected root folder exists
		found := false
		for _, root := range roots {
			if root.Path == expectedPath {
				found = true
				if root.Accessible {
					fmt.Printf("  %s %s → %s  %s\n", ui.Ok("✓"), titleCase(ac.service), root.Path,
						ui.Dim(ui.FmtSize(root.FreeSpace)+" free"))
					r.pass()
				} else {
					fmt.Printf("  %s %s → %s %s\n", ui.Err("✗"), titleCase(ac.service), root.Path,
						ui.Err("inaccessible"))
					r.errf("%s → root folder %s exists but is not accessible", titleCase(ac.service), root.Path)
				}
				break
			}
		}

		if !found {
			// Auto-create root folder
			fmt.Printf("  %s %s → Adding root folder %s\n", ui.GoldText("↻"), titleCase(ac.service), expectedPath)

			if err := client.AddRootFolder(expectedPath); err != nil {
				r.errf("%s → failed to create root folder: %v", titleCase(ac.service), err)
				continue
			}

			fmt.Printf("  %s %s → Root folder %s added\n", ui.Ok("✓"), titleCase(ac.service), expectedPath)
			r.fix()
		}
	}

	return r
}
