package doctor

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/ui"
)

// checkPermissions validates PUID/PGID consistency and directory ownership.
func checkPermissions(r *Result) {
	fmt.Println(ui.Bold("\n  Permissions"))
	fmt.Println(ui.Separator())

	if _, err := exec.LookPath("docker"); err != nil {
		fmt.Printf("  %s %s\n", ui.Dim("—"), ui.Dim("Docker not available (skipping permission checks)"))
		return
	}

	// 1. Check PUID/PGID consistency across containers
	type envInfo struct {
		name string
		puid string
		pgid string
	}

	var envs []envInfo
	for _, svcName := range []string{"radarr", "sonarr", "prowlarr", "qbittorrent", "bazarr", "jellyfin"} {
		if !config.IsConfigured(svcName) {
			continue
		}
		container := config.ContainerName(svcName)
		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)

		out, err := exec.CommandContext(ctx, "docker", "inspect",
			"--format", "{{range .Config.Env}}{{println .}}{{end}}", container).Output()
		cancel()
		if err != nil {
			continue
		}

		info := envInfo{name: svcName}
		for _, line := range strings.Split(string(out), "\n") {
			if strings.HasPrefix(line, "PUID=") {
				info.puid = strings.TrimPrefix(line, "PUID=")
			}
			if strings.HasPrefix(line, "PGID=") {
				info.pgid = strings.TrimPrefix(line, "PGID=")
			}
		}
		if info.puid != "" || info.pgid != "" {
			envs = append(envs, info)
		}
	}

	if len(envs) < 2 {
		fmt.Printf("  %s %s\n", ui.Dim("—"), ui.Dim("Not enough containers to compare PUID/PGID"))
	} else {
		// Check all match the first
		ref := envs[0]
		allMatch := true
		var mismatches []string
		for _, e := range envs[1:] {
			if e.puid != ref.puid || e.pgid != ref.pgid {
				allMatch = false
				mismatches = append(mismatches, fmt.Sprintf("%s(PUID=%s,PGID=%s)", e.name, e.puid, e.pgid))
			}
		}

		if allMatch {
			r.ChecksPassed++
			fmt.Printf("  %s PUID/PGID consistent: PUID=%s PGID=%s across %d services\n",
				ui.Ok("✓"), ref.puid, ref.pgid, len(envs))
		} else {
			r.Issues = append(r.Issues, Issue{Description:
				fmt.Sprintf("PUID/PGID MISMATCH: %s has PUID=%s PGID=%s but %s differ. "+
					"All containers should use the same PUID/PGID for proper file permissions.",
					ref.name, ref.puid, ref.pgid, strings.Join(mismatches, ", ")),
			})
			fmt.Printf("  %s PUID/PGID mismatch: %s=%s/%s vs %s\n",
				ui.Err("✗"), ref.name, ref.puid, ref.pgid, strings.Join(mismatches, ", "))
		}
	}

	// 2. Check data directory ownership
	dataPath := config.DataPath()
	checkDirOwnership(r, "data", dataPath)

	// 3. Check config directory ownership (admirarr config)
	configDir := filepath.Join(os.Getenv("HOME"), ".config", "admirarr")
	checkDirOwnership(r, "config", configDir)
}

func checkDirOwnership(r *Result, label, path string) {
	if path == "" {
		fmt.Printf("  %s %s dir: %s\n", ui.Dim("—"), label, ui.Dim("not configured"))
		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	out, err := exec.CommandContext(ctx, "stat", "-c", "%U:%G", path).Output()
	if err != nil {
		fmt.Printf("  %s %s dir (%s): %s\n", ui.Dim("—"), label, path, ui.Dim("cannot stat"))
		return
	}

	owner := strings.TrimSpace(string(out))
	r.ChecksPassed++
	fmt.Printf("  %s %s dir ownership: %s → %s\n", ui.Ok("✓"), label, path, owner)
}
