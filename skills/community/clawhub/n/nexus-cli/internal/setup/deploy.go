package setup

import (
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/charmbracelet/huh"
	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/migrate"
	"github.com/maxtechera/admirarr/internal/ui"
)

// checkNativeReachable tries api.CheckReachable first (uses config host),
// then falls back to checking on remoteHost if provided.
func checkNativeReachable(name, remoteHost string, port int) bool {
	if api.CheckReachable(name) {
		return true
	}
	if remoteHost == "" {
		return false
	}
	// Try the remote host IP directly
	c := &http.Client{Timeout: 3 * time.Second}
	url := fmt.Sprintf("http://%s:%d/ping", remoteHost, port)
	resp, err := c.Get(url)
	if err != nil {
		return false
	}
	resp.Body.Close()
	return resp.StatusCode == 200
}

// DeployStack runs Phase 2: deploy missing services via Docker Compose.
func DeployStack(state *SetupState) StepResult {
	r := StepResult{Name: "Deploy Stack"}

	// Check Docker is available
	if err := exec.Command("docker", "version").Run(); err != nil {
		r.errf("Docker not found — install Docker or start Docker Desktop")
		return r
	}

	// Set global host in runtime config if detected
	if state.RemoteHost != "" {
		config.SetGlobalHost(state.RemoteHost)
	}

	// Triage services into detected, reachable (native), and missing
	var detected, reachable, missing []string
	for _, name := range state.SelectedServices {
		svc := state.Services[name]
		if svc == nil {
			continue
		}
		if svc.Detected {
			detected = append(detected, name)
		} else {
			// Check if reachable without a container (native/remote)
			def, _ := config.GetServiceDef(name)
			if def.Port > 0 && def.HasAPI && checkNativeReachable(name, state.RemoteHost, def.Port) {
				reachable = append(reachable, name)
				svc.Reachable = true
				// Update service host for remote services
				if state.RemoteHost != "" {
					svc.Host = state.RemoteHost
				}
			} else {
				missing = append(missing, name)
			}
		}
	}

	// Report detected services
	for _, name := range detected {
		fmt.Printf("  %s %-15s %s\n", ui.Ok("✓"), name, ui.Dim("detected"))
		r.pass()
	}

	// Handle reachable-but-not-Docker services (Scenario E)
	if len(reachable) > 0 {
		fmt.Printf("\n  Detected %d services running outside Docker:\n", len(reachable))
		for _, name := range reachable {
			def, _ := config.GetServiceDef(name)
			fmt.Printf("    %s %-15s %s\n", ui.Dim("•"), name, ui.Dim(fmt.Sprintf("native, :%d reachable", def.Port)))
		}

		choice := "keep"
		if state.AutoMode {
			// Auto mode: keep existing native deployments
		} else {
			form := huh.NewForm(huh.NewGroup(
				huh.NewSelect[string]().
					Title("What would you like to do?").
					Options(
						huh.NewOption("Keep existing deployment (configure as-is)", "keep"),
						huh.NewOption("Migrate to Docker (deploy containers)", "migrate"),
					).
					Value(&choice),
			))
			if err := form.Run(); err != nil {
				choice = "keep"
			}
		}

		if choice == "migrate" {
			fmt.Printf("\n  %s Stop native services before deploying Docker containers:\n", ui.Warn("!"))
			for _, name := range reachable {
				fmt.Printf("    sudo systemctl stop %s\n", name)
			}
			fmt.Println()
			missing = append(missing, reachable...)
		} else {
			for _, name := range reachable {
				fmt.Printf("  %s %-15s %s\n", ui.Ok("✓"), name, ui.Dim("native (kept)"))
				r.pass()
			}
		}
	}

	// Early exit if nothing to deploy
	if len(missing) == 0 {
		if len(detected) > 0 || len(reachable) > 0 {
			fmt.Printf("\n  %s All services detected, nothing to deploy\n", ui.Ok("✓"))
		}
		return r
	}

	// VPN prompt (if gluetun or qbittorrent in missing)
	needsVPN := false
	for _, name := range missing {
		if name == "gluetun" || name == "qbittorrent" {
			needsVPN = true
			break
		}
	}
	if needsVPN {
		promptVPN(state)
	}

	// Generate compose
	composeOpts := migrate.ComposeOpts{
		DataDir:     state.DataPath,
		ConfigDir:   state.ConfigDir,
		TZ:          state.Timezone,
		PUID:        fmt.Sprintf("%d", os.Getuid()),
		PGID:        fmt.Sprintf("%d", os.Getgid()),
		VPNProvider: state.VPNProvider,
		VPNType:     state.VPNType,
		VPNCreds:    state.VPNCreds,
	}

	composeContent := migrate.GenerateCompose(missing, composeOpts)

	// Write files
	composePath := filepath.Join(state.ComposeDir, "docker-compose.yml")
	envPath := filepath.Join(state.ComposeDir, ".env")

	// Generate .env with merge (preserves existing VPN creds, custom vars)
	envContent := migrate.GenerateEnvFile(composeOpts, envPath)

	if err := os.MkdirAll(state.ComposeDir, 0755); err != nil {
		r.errf("cannot create compose directory: %v", err)
		return r
	}

	// Backup existing compose file
	if _, err := os.Stat(composePath); err == nil {
		backup := composePath + fmt.Sprintf(".bak.%s", time.Now().Format("20060102-150405"))
		if err := os.Rename(composePath, backup); err == nil {
			fmt.Printf("  %s Backed up existing compose to %s\n", ui.Dim("→"), filepath.Base(backup))
		}
	}

	if err := os.WriteFile(composePath, []byte(composeContent), 0644); err != nil {
		r.errf("cannot write docker-compose.yml: %v", err)
		return r
	}
	fmt.Printf("  %s Written %s\n", ui.Ok("✓"), composePath)

	if err := os.WriteFile(envPath, []byte(envContent), 0644); err != nil {
		r.errf("cannot write .env: %v", err)
		return r
	}
	fmt.Printf("  %s Written %s\n", ui.Ok("✓"), envPath)

	// Docker compose up
	var deployErr error
	ui.SpinWhile("Deploying containers", func() error {
		// Try compose V2 first, fall back to V1
		cmd := exec.Command("docker", "compose", "-f", composePath, "up", "-d")
		cmd.Dir = state.ComposeDir
		out, err := cmd.CombinedOutput()
		if err != nil {
			// Try docker-compose V1
			cmd2 := exec.Command("docker-compose", "-f", composePath, "up", "-d")
			cmd2.Dir = state.ComposeDir
			out2, err2 := cmd2.CombinedOutput()
			if err2 != nil {
				deployErr = fmt.Errorf("%s\n%s", strings.TrimSpace(string(out)), strings.TrimSpace(string(out2)))
				return deployErr
			}
		} else {
			_ = out
		}
		return nil
	})

	if deployErr != nil {
		r.errf("docker compose up failed: %v", deployErr)
		return r
	}

	// Wait for containers to come up (60s max, poll every 3s)
	ui.SpinWhile("Waiting for containers to start", func() error {
		deadline := time.Now().Add(60 * time.Second)
		for time.Now().Before(deadline) {
			allUp := true
			for _, name := range missing {
				container := config.ContainerName(name)
				out, err := exec.Command("docker", "ps", "--filter",
					fmt.Sprintf("name=%s", container), "--format", "{{.Status}}").Output()
				if err != nil || !strings.HasPrefix(strings.TrimSpace(string(out)), "Up") {
					allUp = false
					break
				}
			}
			if allUp {
				return nil
			}
			time.Sleep(3 * time.Second)
		}
		return nil // timeout is a warning, not an error
	})

	// Post-deploy stabilization — services need time to generate config files
	ui.SpinWhile("Waiting for services to stabilize", func() error {
		time.Sleep(5 * time.Second)
		return nil
	})

	// Re-detect services
	out, err := exec.Command("docker", "ps", "-a", "--format", "{{.Names}}").Output()
	if err == nil {
		containers := strings.ToLower(string(out))
		for _, name := range missing {
			container := config.ContainerName(name)
			svc := state.Services[name]
			if svc == nil {
				continue
			}
			if strings.Contains(containers, strings.ToLower(container)) {
				svc.Detected = true
				svc.IsDocker = true
				fmt.Printf("  %s %-15s %s\n", ui.Ok("✓"), name, ui.GoldText("deployed"))
				r.fix()
			} else {
				fmt.Printf("  %s %-15s %s\n", ui.Err("✗"), name, ui.Err("container not found after deploy"))
				r.errf("%s: container did not start", name)
			}
		}
	}

	return r
}

// vpnNeedsAddresses returns true for providers that require WIREGUARD_ADDRESSES.
func vpnNeedsAddresses(provider string) bool {
	return provider == "mullvad" || provider == "surfshark"
}

func promptVPN(state *SetupState) {
	if state.AutoMode {
		state.VPNProvider = "mullvad"
		state.VPNType = "wireguard"
		fmt.Printf("  %s VPN: %s (%s) %s\n", ui.Ok("✓"), state.VPNProvider, state.VPNType, ui.Dim("(auto)"))
		fmt.Printf("  %s VPN credentials not set — add them to .env before starting\n", ui.Warn("!"))
		return
	}

	var provider string
	form := huh.NewForm(huh.NewGroup(
		huh.NewSelect[string]().
			Title("VPN Provider").
			Options(
				huh.NewOption("Mullvad", "mullvad"),
				huh.NewOption("NordVPN", "nordvpn"),
				huh.NewOption("Surfshark", "surfshark"),
				huh.NewOption("ProtonVPN", "protonvpn"),
				huh.NewOption("Private Internet Access", "private internet access"),
				huh.NewOption("Custom", "custom"),
			).
			Value(&provider),
	))
	if err := form.Run(); err != nil {
		provider = "mullvad"
	}
	state.VPNProvider = provider

	var vpnType string
	form = huh.NewForm(huh.NewGroup(
		huh.NewSelect[string]().
			Title("VPN Type").
			Options(
				huh.NewOption("WireGuard (recommended)", "wireguard"),
				huh.NewOption("OpenVPN", "openvpn"),
			).
			Value(&vpnType),
	))
	if err := form.Run(); err != nil {
		vpnType = "wireguard"
	}
	state.VPNType = vpnType

	fmt.Printf("  %s VPN: %s (%s)\n", ui.Ok("✓"), state.VPNProvider, state.VPNType)

	// Collect provider-specific credentials
	promptVPNCreds(state)
}

func promptVPNCreds(state *SetupState) {
	if state.VPNCreds == nil {
		state.VPNCreds = make(map[string]string)
	}
	if state.VPNType == "wireguard" {
		var privateKey string
		form := huh.NewForm(huh.NewGroup(
			huh.NewInput().
				Title("WireGuard Private Key").
				Description("From your VPN provider's WireGuard config").
				Value(&privateKey),
		))
		if err := form.Run(); err == nil && privateKey != "" {
			state.VPNCreds["WIREGUARD_PRIVATE_KEY"] = privateKey
		}

		if vpnNeedsAddresses(state.VPNProvider) {
			var addresses string
			form = huh.NewForm(huh.NewGroup(
				huh.NewInput().
					Title("WireGuard Addresses").
					Description("Interface address (e.g. 10.64.0.1/32)").
					Value(&addresses),
			))
			if err := form.Run(); err == nil && addresses != "" {
				state.VPNCreds["WIREGUARD_ADDRESSES"] = addresses
			}
		}
	} else {
		// OpenVPN
		var username string
		form := huh.NewForm(huh.NewGroup(
			huh.NewInput().
				Title("OpenVPN Username").
				Value(&username),
		))
		if err := form.Run(); err == nil && username != "" {
			state.VPNCreds["OPENVPN_USER"] = username
		}

		var password string
		form = huh.NewForm(huh.NewGroup(
			huh.NewInput().
				Title("OpenVPN Password").
				EchoMode(huh.EchoModePassword).
				Value(&password),
		))
		if err := form.Run(); err == nil && password != "" {
			state.VPNCreds["OPENVPN_PASSWORD"] = password
		}
	}

	// Optional: server countries
	var countries string
	form := huh.NewForm(huh.NewGroup(
		huh.NewInput().
			Title("Server Countries (optional)").
			Description("Comma-separated, e.g. US,NL — leave empty for auto").
			Value(&countries),
	))
	if err := form.Run(); err == nil && countries != "" {
		state.VPNCreds["SERVER_COUNTRIES"] = countries
	}

	if len(state.VPNCreds) > 0 {
		fmt.Printf("  %s VPN credentials collected (%d vars)\n", ui.Ok("✓"), len(state.VPNCreds))
	}
}
