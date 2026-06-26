package setup

import (
	"context"
	"fmt"
	"net/url"
	"os/exec"
	"time"

	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/ui"
)

// WireBazarr runs Phase 9: connect Bazarr to Radarr/Sonarr.
func WireBazarr(state *SetupState) StepResult {
	r := StepResult{Name: "Bazarr Wiring"}

	svc := state.Services["bazarr"]
	if svc == nil || !svc.Reachable {
		fmt.Printf("  %s Bazarr %s\n", ui.Dim("—"), ui.Dim("skipped (not in stack or unreachable)"))
		r.skip()
		return r
	}

	if state.Keys["bazarr"] == "" {
		fmt.Printf("  %s Bazarr %s\n", ui.Dim("—"), ui.Dim("skipped (no API key)"))
		r.skip()
		return r
	}

	// Read current settings via API to check if already wired
	var settings map[string]interface{}
	if err := api.GetJSON("bazarr", "api/system/settings", nil, &settings); err != nil {
		r.errf("Bazarr: cannot fetch settings: %v", err)
		return r
	}

	changed := false

	// Check/wire Radarr
	if radarrSvc := state.Services["radarr"]; radarrSvc != nil && radarrSvc.Reachable && state.Keys["radarr"] != "" {
		if wireBazarrService(state, &r, settings, "radarr") {
			changed = true
		}
	} else {
		fmt.Printf("  %s Bazarr → Radarr %s\n", ui.Dim("—"), ui.Dim("skipped (not reachable)"))
	}

	// Check/wire Sonarr
	if sonarrSvc := state.Services["sonarr"]; sonarrSvc != nil && sonarrSvc.Reachable && state.Keys["sonarr"] != "" {
		if wireBazarrService(state, &r, settings, "sonarr") {
			changed = true
		}
	} else {
		fmt.Printf("  %s Bazarr → Sonarr %s\n", ui.Dim("—"), ui.Dim("skipped (not reachable)"))
	}

	// Check if use_radarr/use_sonarr flags are enabled (they must be for Bazarr to connect)
	general, _ := settings["general"].(map[string]interface{})
	if general != nil {
		for _, svc := range []string{"radarr", "sonarr"} {
			flag := fmt.Sprintf("use_%s", svc)
			if state.Services[svc] != nil && state.Services[svc].Reachable {
				if v, ok := general[flag]; ok && v == false {
					general[flag] = true
					settings["general"] = general
					changed = true
				}
			}
		}
	}

	// Bazarr's API POST doesn't persist settings; we must edit config.yaml directly
	if changed {
		if err := writeBazarrConfig(state, settings); err != nil {
			r.errf("Bazarr: failed to write config: %v", err)
		}
	}

	return r
}

// wireBazarrService checks and wires a single service (radarr/sonarr) in Bazarr settings.
// Returns true if the settings map was modified.
func wireBazarrService(state *SetupState, r *StepResult, settings map[string]interface{}, service string) bool {
	section, _ := settings[service].(map[string]interface{})
	if section == nil {
		section = make(map[string]interface{})
	}

	// Parse expected values — for Bazarr in Docker, use the host IP that
	// the container can reach (not container names, since Bazarr needs to
	// talk to services that may be native/remote).
	internalURL := bazarrTargetURL(state, service)
	parsed, _ := url.Parse(internalURL)
	expectedHost := parsed.Hostname()
	expectedPort := config.ServicePort(service)
	expectedKey := state.Keys[service]

	// Check current values
	currentHost := fmt.Sprintf("%v", section["ip"])
	currentPort := fmt.Sprintf("%v", section["port"])
	currentKey := fmt.Sprintf("%v", section["apikey"])

	if currentHost == expectedHost &&
		currentPort == fmt.Sprintf("%d", expectedPort) &&
		currentKey == expectedKey {
		fmt.Printf("  %s Bazarr → %s connected\n", ui.Ok("✓"), service)
		r.pass()
		return false
	}

	// Update in the settings map (used for config file write)
	section["ip"] = expectedHost
	section["port"] = expectedPort
	section["apikey"] = expectedKey
	section["base_url"] = ""
	settings[service] = section

	fmt.Printf("  %s Bazarr → %s configured (%s:%d)\n", ui.Ok("✓"), service, expectedHost, expectedPort)
	r.fix()
	return true
}

// bazarrTargetURL returns the URL that Bazarr should use to reach a target service.
// Since Bazarr runs in Docker, it needs to use:
//   - Docker host gateway for native services on the same host
//   - Container name for Docker services on the same Docker network
//   - Remote IP for remote services
func bazarrTargetURL(state *SetupState, service string) string {
	svc := state.Services[service]
	def, _ := config.GetServiceDef(service)
	port := def.Port
	if svc != nil && svc.Port > 0 {
		port = svc.Port
	}

	// Remote services — use their host IP directly
	if svc != nil && svc.Host != "" && svc.Host != "localhost" && svc.Host != "127.0.0.1" {
		return fmt.Sprintf("http://%s:%d", svc.Host, port)
	}

	// Docker services — use container name
	if svc != nil && svc.IsDocker {
		return fmt.Sprintf("http://%s:%d", config.ContainerName(service), port)
	}

	// Native services on the same host — Bazarr (Docker) needs host.docker.internal
	// or the Docker gateway IP to reach them
	if state.RemoteHost != "" {
		return fmt.Sprintf("http://%s:%d", state.RemoteHost, port)
	}

	// Fallback: use host.docker.internal which Docker Desktop provides,
	// or the default gateway on Linux
	return fmt.Sprintf("http://host.docker.internal:%d", port)
}

// writeBazarrConfig writes the updated settings to Bazarr's config.yaml via docker exec,
// then restarts the container so changes take effect.
func writeBazarrConfig(state *SetupState, settings map[string]interface{}) error {
	bazarrSvc := state.Services["bazarr"]
	container := config.ContainerName("bazarr")

	if bazarrSvc != nil && bazarrSvc.IsDocker {
		return writeBazarrConfigDocker(container, settings)
	}

	// For native Bazarr, we'd need to find and edit the config file on disk.
	// This is less common, so just inform the user.
	fmt.Printf("  %s Bazarr is not Docker — configure manually in Bazarr Settings\n", ui.Warn("!"))
	return nil
}

// writeBazarrConfigDocker stops Bazarr, edits config.yaml via sed, then starts it again.
// Bazarr overwrites its config on shutdown, so we must stop it first.
func writeBazarrConfigDocker(container string, settings map[string]interface{}) error {
	configPath := "/config/config/config.yaml"

	// Stop Bazarr first — it writes config to disk on shutdown,
	// so if we edit while running, our changes get overwritten on restart.
	fmt.Printf("  %s Stopping Bazarr for config update…\n", ui.GoldText("⟳"))
	stopCtx, stopCancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer stopCancel()
	stopCmd := exec.CommandContext(stopCtx, "docker", "stop", container)
	if err := stopCmd.Run(); err != nil {
		return fmt.Errorf("failed to stop bazarr: %v", err)
	}

	// Now edit the config file while the container is stopped.
	// Use docker cp + host-side editing since container is stopped.
	wiredServices := []string{}
	for _, service := range []string{"radarr", "sonarr"} {
		section, ok := settings[service].(map[string]interface{})
		if !ok {
			continue
		}

		ip, _ := section["ip"].(string)
		apikey, _ := section["apikey"].(string)
		port := fmt.Sprintf("%v", section["port"])

		if ip == "" || apikey == "" {
			continue
		}

		if err := writeBazarrConfigSed(container, configPath, service, ip, port, apikey); err != nil {
			// Start Bazarr back even on error
			startCmd := exec.Command("docker", "start", container)
			startCmd.Run()
			return err
		}
		wiredServices = append(wiredServices, service)
	}

	// Enable use_radarr/use_sonarr in the general section
	if err := enableBazarrServices(container, configPath, wiredServices); err != nil {
		startCmd := exec.Command("docker", "start", container)
		startCmd.Run()
		return err
	}

	// Start Bazarr back up
	fmt.Printf("  %s Starting Bazarr…\n", ui.GoldText("⟳"))
	startCtx, startCancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer startCancel()
	startCmd := exec.CommandContext(startCtx, "docker", "start", container)
	if err := startCmd.Run(); err != nil {
		return fmt.Errorf("failed to start bazarr: %v", err)
	}

	// Wait for Bazarr to come back
	ui.SpinWhile("Waiting for Bazarr to restart", func() error {
		time.Sleep(5 * time.Second)
		return nil
	})
	fmt.Printf("  %s Bazarr restarted with updated config\n", ui.Ok("✓"))
	return nil
}

// writeBazarrConfigSed edits Bazarr's config.yaml using docker cp + host-side sed.
// Works on both running and stopped containers.
func writeBazarrConfigSed(container, configPath, service, ip, port, apikey string) error {
	// Copy config file out of the container
	tmpFile := fmt.Sprintf("/tmp/bazarr_config_%d.yaml", time.Now().UnixNano())
	defer func() {
		exec.Command("rm", "-f", tmpFile).Run()
	}()

	cpOut := exec.Command("docker", "cp", container+":"+configPath, tmpFile)
	if out, err := cpOut.CombinedOutput(); err != nil {
		return fmt.Errorf("docker cp out failed: %v (%s)", err, string(out))
	}

	// Use sed on the host to update the config
	sedCmds := []string{
		fmt.Sprintf(`/^%s:/,/^[a-z]/{s/^  ip: .*/  ip: %s/}`, service, ip),
		fmt.Sprintf(`/^%s:/,/^[a-z]/{s/^  port: .*/  port: %s/}`, service, port),
		fmt.Sprintf(`/^%s:/,/^[a-z]/{s/^  apikey: .*/  apikey: %s/}`, service, apikey),
		fmt.Sprintf(`/^%s:/,/^[a-z]/{s|^  base_url: .*|  base_url: |}`, service),
	}

	for _, sedExpr := range sedCmds {
		cmd := exec.Command("sed", "-i", sedExpr, tmpFile)
		if out, err := cmd.CombinedOutput(); err != nil {
			return fmt.Errorf("sed failed for %s: %v (%s)", service, err, string(out))
		}
	}

	// Copy config file back into the container
	cpIn := exec.Command("docker", "cp", tmpFile, container+":"+configPath)
	if out, err := cpIn.CombinedOutput(); err != nil {
		return fmt.Errorf("docker cp in failed: %v (%s)", err, string(out))
	}

	return nil
}

// enableBazarrServices sets use_radarr/use_sonarr to true in Bazarr's general section.
func enableBazarrServices(container, configPath string, services []string) error {
	tmpFile := fmt.Sprintf("/tmp/bazarr_enable_%d.yaml", time.Now().UnixNano())
	defer func() {
		exec.Command("rm", "-f", tmpFile).Run()
	}()

	cpOut := exec.Command("docker", "cp", container+":"+configPath, tmpFile)
	if out, err := cpOut.CombinedOutput(); err != nil {
		return fmt.Errorf("docker cp out failed: %v (%s)", err, string(out))
	}

	for _, svc := range services {
		flag := fmt.Sprintf("use_%s", svc)
		sedExpr := fmt.Sprintf(`/^general:/,/^[a-z]/{s/^  %s: false/  %s: true/}`, flag, flag)
		cmd := exec.Command("sed", "-i", sedExpr, tmpFile)
		if out, err := cmd.CombinedOutput(); err != nil {
			return fmt.Errorf("sed failed enabling %s: %v (%s)", flag, err, string(out))
		}
	}

	cpIn := exec.Command("docker", "cp", tmpFile, container+":"+configPath)
	if out, err := cpIn.CombinedOutput(); err != nil {
		return fmt.Errorf("docker cp in failed: %v (%s)", err, string(out))
	}

	return nil
}
