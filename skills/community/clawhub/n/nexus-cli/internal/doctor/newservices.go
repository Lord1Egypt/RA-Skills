package doctor

import (
	"context"
	"fmt"
	"os/exec"
	"strings"
	"time"

	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/ui"
)

// checkNewServices validates Profilarr and Watchtower status.
func checkNewServices(r *Result) {
	fmt.Println(ui.Bold("\n  Additional Services"))
	fmt.Println(ui.Separator())

	// 1. Profilarr health
	if config.IsConfigured("profilarr") {
		if api.CheckReachable("profilarr") {
			r.ChecksPassed++
			fmt.Printf("  %s Profilarr: %s\n", ui.Ok("✓"), ui.Ok("reachable"))
		} else {
			r.Issues = append(r.Issues, Issue{Description:
				"PROFILARR UNREACHABLE: Profilarr is configured but not responding. Check container logs.",
			})
			fmt.Printf("  %s Profilarr: %s\n", ui.Err("✗"), ui.Err("unreachable"))
		}
	} else {
		fmt.Printf("  %s Profilarr: %s\n", ui.Dim("—"), ui.Dim("not configured"))
	}

	// 2. Watchtower running
	checkWatchtower(r)
}

func checkWatchtower(r *Result) {
	if _, err := exec.LookPath("docker"); err != nil {
		fmt.Printf("  %s Watchtower: %s\n", ui.Dim("—"), ui.Dim("Docker not available"))
		return
	}

	container := config.ContainerName("watchtower")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	out, err := exec.CommandContext(ctx, "docker", "inspect",
		"--format", "{{.State.Status}}", container).Output()
	if err != nil {
		if config.IsConfigured("watchtower") {
			r.Issues = append(r.Issues, Issue{Description:
				fmt.Sprintf("WATCHTOWER: Container %q not found. Auto-updates are not running.", container),
			})
			fmt.Printf("  %s Watchtower: %s\n", ui.Err("✗"), ui.Err("container not found"))
		} else {
			fmt.Printf("  %s Watchtower: %s\n", ui.Dim("—"), ui.Dim("not configured"))
		}
		return
	}

	status := strings.TrimSpace(string(out))
	if status == "running" {
		r.ChecksPassed++
		fmt.Printf("  %s Watchtower: %s\n", ui.Ok("✓"), ui.Ok("running (auto-updates enabled)"))
	} else {
		r.Issues = append(r.Issues, Issue{Description:
			fmt.Sprintf("WATCHTOWER: Container status=%s. Auto-updates are not active. Try: docker start %s", status, container),
		})
		fmt.Printf("  %s Watchtower: %s (%s)\n", ui.Err("✗"), ui.Err("not running"), status)
	}
}
