package setup

import (
	"fmt"

	"github.com/charmbracelet/huh"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/ui"
)

// SelectServices runs Phase 0: service tier selection.
func SelectServices(state *SetupState) StepResult {
	r := StepResult{Name: "Service Selection"}

	coreNames := config.ServicesByTier("core")
	optionalNames := config.ServicesByTier("optional")

	// In auto mode, use all configured services + core defaults
	if state.AutoMode {
		selected := coreNames
		// Add any optional services that are already configured/detected
		for _, name := range optionalNames {
			if config.IsConfigured(name) {
				selected = append(selected, name)
			}
		}
		state.SelectedServices = selected
		fmt.Printf("  %s Auto-selected %d services\n", ui.Ok("✓"), len(selected))
		for _, name := range selected {
			fmt.Printf("    %s %s\n", ui.Ok("✓"), name)
		}
		r.pass()
		return r
	}

	// Build options
	var options []huh.Option[string]
	for _, name := range coreNames {
		def, _ := config.GetServiceDef(name)
		label := fmt.Sprintf("%s (%s, :%d)", name, def.Category, def.Port)
		options = append(options, huh.NewOption(label, name).Selected(true))
	}
	for _, name := range optionalNames {
		def, _ := config.GetServiceDef(name)
		label := fmt.Sprintf("%s (%s, :%d) [optional]", name, def.Category, def.Port)
		options = append(options, huh.NewOption(label, name))
	}

	selected := make([]string, len(coreNames))
	copy(selected, coreNames)

	form := huh.NewForm(
		huh.NewGroup(
			huh.NewMultiSelect[string]().
				Title("Select services for your stack").
				Options(options...).
				Value(&selected),
		),
	)

	if err := form.Run(); err != nil {
		// Use defaults on error
		selected = coreNames
	}

	// Validate minimum: media server + at least one *Arr + download client
	hasMedia := false
	hasArr := false
	hasDownload := false
	for _, s := range selected {
		def, ok := config.GetServiceDef(s)
		if !ok {
			continue
		}
		switch {
		case s == "jellyfin" || s == "plex":
			hasMedia = true
		case def.APIVer != "" && def.Category == "management":
			hasArr = true // radarr, sonarr, lidarr, readarr, whisparr
		case s == "qbittorrent" || s == "sabnzbd":
			hasDownload = true
		}
	}

	if !hasMedia || !hasArr || !hasDownload {
		fmt.Printf("  %s Minimum requires: media server + at least one *Arr + download client\n", ui.Warn("!"))
		if !hasMedia {
			selected = append(selected, "jellyfin")
		}
		if !hasArr {
			selected = append(selected, "radarr")
		}
		if !hasDownload {
			selected = append(selected, "qbittorrent")
		}
	}

	state.SelectedServices = selected
	fmt.Printf("  %s Selected %d services\n", ui.Ok("✓"), len(selected))
	for _, name := range selected {
		fmt.Printf("    %s %s\n", ui.Ok("✓"), name)
	}

	r.pass()
	return r
}
