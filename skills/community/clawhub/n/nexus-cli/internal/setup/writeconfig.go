package setup

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/charmbracelet/huh"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/ui"
)

// WriteConfig runs Phase 11: write validated config to disk.
func WriteConfig(state *SetupState) StepResult {
	r := StepResult{Name: "Write Config"}

	configDir := filepath.Join(os.Getenv("HOME"), ".config", "admirarr")
	configPath := filepath.Join(configDir, "config.yaml")

	// Build YAML content
	yaml := buildYAML(state)

	// Preview
	fmt.Printf("  %s %s\n", ui.Bold("Config preview:"), ui.Dim(configPath))
	fmt.Printf("  %s\n", ui.Dim("──────────────────────────────────────────────────"))
	for _, line := range strings.Split(yaml, "\n") {
		fmt.Printf("  %s %s\n", ui.Dim("│"), line)
	}
	fmt.Printf("  %s\n", ui.Dim("──────────────────────────────────────────────────"))

	// Check if file exists
	action := "write"
	if state.AutoMode {
		action = "overwrite"
	} else if _, err := os.Stat(configPath); err == nil {
		var selected string
		form := huh.NewForm(huh.NewGroup(
			huh.NewSelect[string]().
				Title("Config file exists. What to do?").
				Options(
					huh.NewOption("Overwrite", "overwrite"),
					huh.NewOption("Skip", "skip"),
				).
				Value(&selected),
		))
		if err := form.Run(); err != nil || selected == "skip" {
			fmt.Printf("  %s Config write skipped\n", ui.Dim("—"))
			r.skip()
			return r
		}
		action = selected
	} else {
		var confirm bool
		form := huh.NewForm(huh.NewGroup(
			huh.NewConfirm().
				Title("Write config?").
				Value(&confirm),
		))
		if err := form.Run(); err != nil || !confirm {
			r.skip()
			return r
		}
	}

	if action == "skip" {
		r.skip()
		return r
	}

	// Ensure directory exists
	if err := os.MkdirAll(configDir, 0755); err != nil {
		r.errf("cannot create config directory: %v", err)
		return r
	}

	if err := os.WriteFile(configPath, []byte(yaml), 0644); err != nil {
		r.errf("cannot write config: %v", err)
		return r
	}

	fmt.Printf("  %s Written to %s\n", ui.Ok("✓"), configPath)
	r.fix()
	return r
}

func buildYAML(state *SetupState) string {
	dataPath := state.DataPath
	if dataPath == "" {
		dataPath = config.DataPath()
	}

	var b strings.Builder

	b.WriteString("# ─── Admirarr Configuration ───────────────────────────────────────────\n")
	b.WriteString("# Run `admirarr setup` to converge your stack to this desired state.\n\n")

	b.WriteString(fmt.Sprintf("data_path: \"%s\"\n", dataPath))

	if state.RemoteHost != "" {
		b.WriteString(fmt.Sprintf("host: \"%s\"\n", state.RemoteHost))
	}

	if state.ComposeDir != "" {
		b.WriteString(fmt.Sprintf("compose_dir: \"%s\"\n", state.ComposeDir))
	}

	if state.Timezone != "" {
		b.WriteString(fmt.Sprintf("timezone: \"%s\"\n", state.Timezone))
	}

	b.WriteString("\n")

	// Services — only include detected/deployed services
	b.WriteString("# ─── Services ─────────────────────────────────────────────────────────\n")
	b.WriteString("services:\n")

	selected := state.SelectedServices
	if len(selected) == 0 {
		selected = config.AllServiceNames()
	}

	for _, name := range selected {
		svc := state.Services[name]
		if svc == nil || (!svc.Detected && !svc.Reachable) {
			continue
		}
		b.WriteString(fmt.Sprintf("  %s:\n", name))
		b.WriteString(fmt.Sprintf("    port: %d\n", svc.Port))
		host := svc.Host
		if host == "" {
			host = "localhost"
		}
		b.WriteString(fmt.Sprintf("    host: %s\n", host))
		if svc.IsDocker {
			b.WriteString("    type: docker\n")
		} else if svc.Reachable {
			if state.RemoteHost != "" && svc.Host == state.RemoteHost {
				b.WriteString("    type: remote\n")
			} else {
				b.WriteString("    type: native\n")
			}
		}
	}

	// Keys
	b.WriteString("\n# ─── API Keys ─────────────────────────────────────────────────────────\n")
	b.WriteString("keys:\n")
	for _, name := range []string{"jellyfin", "sonarr", "radarr", "prowlarr", "seerr", "bazarr", "tautulli"} {
		key := ""
		if state.Keys != nil {
			key = state.Keys[name]
		}
		if key == "" && state.ManualKeys != nil {
			key = state.ManualKeys[name]
		}
		b.WriteString(fmt.Sprintf("  %s: \"%s\"\n", name, key))
	}

	// Quality profile
	qp := config.QualityProfile()
	if qp == "" {
		qp = "HD-1080p"
	}
	b.WriteString(fmt.Sprintf("\n# ─── Quality ──────────────────────────────────────────────────────────\n"))
	b.WriteString(fmt.Sprintf("quality_profile: \"%s\"\n", qp))

	// Indexers — prefer state.Indexers (from setup) over config
	indexers := config.GetIndexers()
	if len(indexers) == 0 && len(state.Indexers) > 0 {
		indexers = state.Indexers
	}
	if len(indexers) > 0 {
		b.WriteString("\n# ─── Indexers ─────────────────────────────────────────────────────────\n")
		b.WriteString("# Indexers NOT listed here will be removed during sync.\n")
		b.WriteString("indexers:\n")
		for name, ic := range indexers {
			if ic.BaseURL == "" && !ic.Flare && len(ic.ExtraFields) == 0 {
				b.WriteString(fmt.Sprintf("  %q: {}\n", name))
			} else {
				b.WriteString(fmt.Sprintf("  %q:\n", name))
				if ic.Flare {
					b.WriteString("    flare: true\n")
				}
				if ic.BaseURL != "" {
					b.WriteString(fmt.Sprintf("    base_url: \"%s\"\n", ic.BaseURL))
				}
				if len(ic.ExtraFields) > 0 {
					b.WriteString("    extra_fields:\n")
					for k, v := range ic.ExtraFields {
						b.WriteString(fmt.Sprintf("      %s: \"%v\"\n", k, v))
					}
				}
			}
		}
	}

	return b.String()
}
