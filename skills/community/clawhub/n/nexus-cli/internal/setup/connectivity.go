package setup

import (
	"fmt"
	"os/exec"
	"strings"
	"time"

	"net/http"

	"github.com/charmbracelet/huh"
	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/ui"
)

// CheckConnectivity runs Phase 3: service reachability and restart offers.
func CheckConnectivity(state *SetupState) StepResult {
	r := StepResult{Name: "Service Connectivity"}

	selected := state.SelectedServices
	if len(selected) == 0 {
		selected = config.AllServiceNames()
	}

	for _, name := range selected {
		svc := state.Services[name]
		if svc == nil || (!svc.Detected && !svc.Reachable) {
			fmt.Printf("  %s %-15s %s\n", ui.Dim("—"), name, ui.Dim("skipped (not detected)"))
			r.skip()
			continue
		}

		// Skip portless services
		def, _ := config.GetServiceDef(name)
		if def.Port == 0 {
			r.skip()
			continue
		}

		if api.CheckReachable(name) || checkOnRemoteHost(state.RemoteHost, def.Port) {
			svc.Reachable = true
			fmt.Printf("  %s %-15s %s\n", ui.Ok("✓"), name, ui.Ok("reachable"))
			r.pass()
			continue
		}

		fmt.Printf("  %s %-15s %s\n", ui.Err("✗"), name, ui.Err("unreachable"))

		// In auto mode, always attempt restart
		confirm := state.AutoMode
		if !confirm {
			form := huh.NewForm(
				huh.NewGroup(
					huh.NewConfirm().
						Title(fmt.Sprintf("%s is unreachable. Attempt to start/restart?", name)).
						Value(&confirm),
				),
			)
			if err := form.Run(); err != nil {
				confirm = false
			}
		}

		if !confirm {
			r.errf("%s unreachable (user skipped restart)", name)
			continue
		}

		if !svc.IsDocker {
			if svc.Host != "" && svc.Host != "localhost" && svc.Host != "127.0.0.1" {
				fmt.Printf("    %s Cannot restart remote service %s — restart it on the remote host\n", ui.Warn("!"), name)
			} else {
				fmt.Printf("    %s %s is a native service — try: sudo systemctl restart %s\n", ui.Warn("!"), name, name)
			}
			r.errf("%s unreachable (not a Docker service, cannot auto-restart)", name)
			continue
		}

		container := config.ContainerName(name)
		out, err := exec.Command("docker", "start", container).CombinedOutput()
		if err != nil {
			fmt.Printf("    %s %s\n", ui.Err("Failed:"), strings.TrimSpace(string(out)))
			r.errf("%s restart failed", name)
			continue
		}
		fmt.Printf("    %s docker start %s\n", ui.Dim("→"), container)

		// Wait and retry with backoff
		reachable := false
		for _, wait := range []time.Duration{1, 2, 4} {
			time.Sleep(wait * time.Second)
			if api.CheckReachable(name) {
				reachable = true
				break
			}
		}
		if reachable {
			svc.Reachable = true
			fmt.Printf("  %s %-15s %s\n", ui.Ok("✓"), name, ui.GoldText("started"))
			r.fix()
		} else {
			r.errf("%s still unreachable after restart", name)
		}
	}

	return r
}

func checkOnRemoteHost(remoteHost string, port int) bool {
	if remoteHost == "" || port == 0 {
		return false
	}
	c := &http.Client{Timeout: 3 * time.Second}
	resp, err := c.Get(fmt.Sprintf("http://%s:%d/ping", remoteHost, port))
	if err != nil {
		return false
	}
	resp.Body.Close()
	return resp.StatusCode == 200
}
