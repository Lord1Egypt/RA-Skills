package doctor

import (
	"context"
	"fmt"
	"os/exec"
	"strings"
	"time"

	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/maxtechera/admirarr/internal/wire"
)

// checkVPN validates Gluetun VPN routing and connectivity.
// Checks: Gluetun healthy, VPN connected, qBit routed through Gluetun, qBit IP differs from host.
func checkVPN(r *Result) {
	fmt.Println(ui.Bold("\n  VPN / Gluetun"))
	fmt.Println(ui.Separator())

	// Check if Gluetun is configured
	if !config.IsConfigured("gluetun") {
		fmt.Printf("  %s %s\n", ui.Dim("—"), ui.Dim("Gluetun not configured (skipping VPN checks)"))
		return
	}

	// 1. Check Gluetun container health
	gluetunContainer := config.ContainerName("gluetun")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	out, err := exec.CommandContext(ctx, "docker", "inspect",
		"--format", "{{.State.Health.Status}}", gluetunContainer).Output()
	if err != nil {
		fmt.Printf("  %s Gluetun container %s\n", ui.Dim("—"), ui.Dim("not inspectable (Docker unavailable or container missing)"))
	} else {
		health := strings.TrimSpace(string(out))
		if health == "healthy" {
			r.ChecksPassed++
			fmt.Printf("  %s Gluetun container: %s\n", ui.Ok("✓"), ui.Ok("healthy"))
		} else {
			r.Issues = append(r.Issues, Issue{Description:
				fmt.Sprintf("GLUETUN UNHEALTHY: container health=%s. Check Gluetun logs: docker logs --tail 30 %s", health, gluetunContainer),
			})
			fmt.Printf("  %s Gluetun container: %s\n", ui.Err("✗"), ui.Err(health))
		}
	}

	// 2. Check VPN status via Gluetun control server
	vpn := wire.GetVPNStatus()
	if vpn.Err != nil {
		fmt.Printf("  %s VPN status: %s\n", ui.Dim("—"), ui.Dim(vpn.Err.Error()))
	} else if vpn.Connected {
		r.ChecksPassed++
		detail := "connected"
		if vpn.IP != "" {
			detail += fmt.Sprintf(", IP=%s", vpn.IP)
		}
		if vpn.Country != "" {
			detail += fmt.Sprintf(" (%s)", vpn.Country)
		}
		fmt.Printf("  %s VPN: %s\n", ui.Ok("✓"), detail)
	} else {
		r.Issues = append(r.Issues, Issue{Description:
			"VPN DISCONNECTED: Gluetun reports VPN is not running. Check VPN credentials and provider configuration.",
		})
		fmt.Printf("  %s VPN: %s\n", ui.Err("✗"), ui.Err("disconnected"))
	}

	// 3. Check qBittorrent routes through Gluetun
	routeResult := wire.CheckVPNRoute()
	switch routeResult.Action {
	case "ok":
		r.ChecksPassed++
		fmt.Printf("  %s qBittorrent VPN routing: %s\n", ui.Ok("✓"), routeResult.Detail)
	case "skipped":
		fmt.Printf("  %s qBittorrent VPN routing: %s\n", ui.Dim("—"), ui.Dim(routeResult.Detail))
	case "failed":
		r.Issues = append(r.Issues, Issue{Description:
			fmt.Sprintf("VPN ROUTING: %s", routeResult.Detail),
		})
		fmt.Printf("  %s qBittorrent VPN routing: %s\n", ui.Err("✗"), ui.Err(routeResult.Detail))
	}

	// 4. Check VPN provider env var
	ctx2, cancel2 := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel2()

	providerOut, err := exec.CommandContext(ctx2, "docker", "inspect",
		"--format", "{{range .Config.Env}}{{println .}}{{end}}", gluetunContainer).Output()
	if err == nil {
		hasProvider := false
		for _, line := range strings.Split(string(providerOut), "\n") {
			if strings.HasPrefix(line, "VPN_SERVICE_PROVIDER=") {
				provider := strings.TrimPrefix(line, "VPN_SERVICE_PROVIDER=")
				if provider != "" {
					hasProvider = true
					r.ChecksPassed++
					fmt.Printf("  %s VPN provider: %s\n", ui.Ok("✓"), provider)
				}
				break
			}
		}
		if !hasProvider {
			r.Issues = append(r.Issues, Issue{Description:
				"VPN PROVIDER: VPN_SERVICE_PROVIDER not set on Gluetun container.",
			})
			fmt.Printf("  %s VPN provider: %s\n", ui.Err("✗"), ui.Err("not configured"))
		}
	}
}
