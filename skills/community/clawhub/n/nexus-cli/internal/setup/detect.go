package setup

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	"github.com/charmbracelet/huh"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/ui"
)

// Detect runs Phase 1: environment detection.
func Detect(state *SetupState) StepResult {
	r := StepResult{Name: "Environment Detection"}

	// 1. Detect data path
	detectDataPath(state, &r)

	// 2. Detect timezone
	detectTimezone(state, &r)

	// 3. Detect compose directory
	detectComposeDir(state, &r)

	// 4. Detect config directory
	detectConfigDir(state, &r)

	// 5. Detect Remote host IP (WSL2)
	detectRemoteHost(state, &r)

	// 6. Detect installed services via Docker
	detectServices(state, &r)

	return r
}

func detectDataPath(state *SetupState, r *StepResult) {
	currentPath := config.DataPath()

	if state.AutoMode {
		state.DataPath = currentPath
		fmt.Printf("  %s Data path: %s\n", ui.Ok("✓"), state.DataPath)
		r.pass()
		return
	}

	var confirm bool
	form := huh.NewForm(
		huh.NewGroup(
			huh.NewConfirm().
				Title(fmt.Sprintf("Data path is %s — correct?", currentPath)).
				Value(&confirm),
		),
	)
	if err := form.Run(); err != nil {
		state.DataPath = currentPath
		r.pass()
		return
	}

	if confirm {
		state.DataPath = currentPath
	} else {
		var path string
		form = huh.NewForm(
			huh.NewGroup(
				huh.NewInput().
					Title("Enter data path (Docker volume root)").
					Placeholder("/data").
					Value(&path),
			),
		)
		if err := form.Run(); err != nil || path == "" {
			path = currentPath
		}
		state.DataPath = path
	}

	fmt.Printf("  %s Data path: %s\n", ui.Ok("✓"), state.DataPath)
	r.pass()
}

func detectTimezone(state *SetupState, r *StepResult) {
	tz := os.Getenv("TZ")
	if tz == "" {
		if data, err := os.ReadFile("/etc/timezone"); err == nil {
			tz = strings.TrimSpace(string(data))
		}
	}
	if tz == "" {
		tz = "UTC"
	}

	if state.AutoMode {
		state.Timezone = tz
		fmt.Printf("  %s Timezone: %s\n", ui.Ok("✓"), state.Timezone)
		r.pass()
		return
	}

	var confirm bool
	form := huh.NewForm(
		huh.NewGroup(
			huh.NewConfirm().
				Title(fmt.Sprintf("Timezone is %s — correct?", tz)).
				Value(&confirm),
		),
	)
	if err := form.Run(); err != nil {
		state.Timezone = tz
		r.pass()
		return
	}

	if confirm {
		state.Timezone = tz
	} else {
		var input string
		form = huh.NewForm(
			huh.NewGroup(
				huh.NewInput().
					Title("Enter timezone (e.g. America/New_York)").
					Placeholder("UTC").
					Value(&input),
			),
		)
		if err := form.Run(); err != nil || input == "" {
			input = tz
		}
		state.Timezone = input
	}

	fmt.Printf("  %s Timezone: %s\n", ui.Ok("✓"), state.Timezone)
	r.pass()
}

func detectComposeDir(state *SetupState, r *StepResult) {
	defaultDir := filepath.Join(os.Getenv("HOME"), "docker")

	if state.AutoMode {
		state.ComposeDir = defaultDir
		fmt.Printf("  %s Compose dir: %s\n", ui.Ok("✓"), state.ComposeDir)
		r.pass()
		return
	}

	var confirm bool
	form := huh.NewForm(
		huh.NewGroup(
			huh.NewConfirm().
				Title(fmt.Sprintf("Compose directory is %s — correct?", defaultDir)).
				Value(&confirm),
		),
	)
	if err := form.Run(); err != nil {
		state.ComposeDir = defaultDir
		r.pass()
		return
	}

	if confirm {
		state.ComposeDir = defaultDir
	} else {
		var input string
		form = huh.NewForm(
			huh.NewGroup(
				huh.NewInput().
					Title("Enter compose directory").
					Placeholder(defaultDir).
					Value(&input),
			),
		)
		if err := form.Run(); err != nil || input == "" {
			input = defaultDir
		}
		state.ComposeDir = input
	}

	fmt.Printf("  %s Compose dir: %s\n", ui.Ok("✓"), state.ComposeDir)
	r.pass()
}

func detectConfigDir(state *SetupState, r *StepResult) {
	defaultDir := filepath.Join(state.ComposeDir, "config")

	if state.AutoMode {
		state.ConfigDir = defaultDir
		fmt.Printf("  %s Config dir: %s\n", ui.Ok("✓"), state.ConfigDir)
		r.pass()
		return
	}

	var confirm bool
	form := huh.NewForm(
		huh.NewGroup(
			huh.NewConfirm().
				Title(fmt.Sprintf("Config directory is %s — correct?", defaultDir)).
				Value(&confirm),
		),
	)
	if err := form.Run(); err != nil {
		state.ConfigDir = defaultDir
		r.pass()
		return
	}

	if confirm {
		state.ConfigDir = defaultDir
	} else {
		var input string
		form = huh.NewForm(
			huh.NewGroup(
				huh.NewInput().
					Title("Enter config directory").
					Placeholder(defaultDir).
					Value(&input),
			),
		)
		if err := form.Run(); err != nil || input == "" {
			input = defaultDir
		}
		state.ConfigDir = input
	}

	fmt.Printf("  %s Config dir: %s\n", ui.Ok("✓"), state.ConfigDir)
	r.pass()
}

func detectServices(state *SetupState, r *StepResult) {
	// Initialize from selected services (Phase 0)
	selected := state.SelectedServices
	if len(selected) == 0 {
		selected = config.AllServiceNames()
	}

	for _, name := range selected {
		def, ok := config.GetServiceDef(name)
		if !ok {
			continue
		}
		state.Services[name] = &ServiceState{
			Host: "localhost",
			Port: def.Port,
		}
	}

	// Detect Docker containers
	out, err := exec.Command("docker", "ps", "-a", "--format", "{{.Names}}").Output()
	if err == nil {
		containers := strings.ToLower(string(out))
		for _, name := range selected {
			container := config.ContainerName(name)
			if strings.Contains(containers, strings.ToLower(container)) {
				if s, ok := state.Services[name]; ok {
					s.Detected = true
					s.IsDocker = true
				}
			}
		}
	}

	detected := 0
	for _, s := range state.Services {
		if s.Detected {
			detected++
		}
	}

	fmt.Printf("  %s Detected %d/%d services\n", ui.Ok("✓"), detected, len(state.Services))

	for _, name := range selected {
		s := state.Services[name]
		if s == nil {
			continue
		}
		status := ui.Ok("✓")
		label := "detected"
		if !s.Detected {
			status = ui.Dim("—")
			label = "not found"
		}
		fmt.Printf("    %s %-15s %s\n", status, name, ui.Dim(label))
	}
	r.pass()
}

func detectRemoteHost(state *SetupState, r *StepResult) {
	// Check if we're in WSL2 by looking for /mnt/c
	if _, err := os.Stat("/mnt/c/Windows"); err != nil {
		return // Not WSL2, skip
	}

	// Try existing config first
	host := config.Host()
	if host != "" && host != "localhost" {
		state.RemoteHost = host
		fmt.Printf("  %s Remote host: %s %s\n", ui.Ok("✓"), host, ui.Dim("(from config)"))
		r.pass()
		return
	}

	// Detect via PowerShell
	out, err := exec.Command("/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
		"-Command",
		"(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {($_.InterfaceAlias -notmatch 'Loopback|vEthernet') -and ($_.IPAddress -match '^(10\\.|172\\.(1[6-9]|2[0-9]|3[01])\\.|192\\.168\\.)')} | Select-Object -First 1).IPAddress",
	).Output()
	if err == nil {
		ip := strings.TrimSpace(strings.TrimRight(string(out), "\r\n"))
		if ip != "" {
			state.RemoteHost = ip
			fmt.Printf("  %s Remote host: %s %s\n", ui.Ok("✓"), ip, ui.Dim("(detected via WSL)"))
			r.pass()
			return
		}
	}

	fmt.Printf("  %s Remote host: %s\n", ui.Dim("—"), ui.Dim("not detected"))
}
