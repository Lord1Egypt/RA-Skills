package doctor

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"

	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/keys"
	"github.com/maxtechera/admirarr/internal/qbit"
	"github.com/maxtechera/admirarr/internal/recyclarr"
	"github.com/maxtechera/admirarr/internal/ui"
)

// Issue represents a diagnostic issue found.
type Issue struct {
	Description string
	Category    string   // e.g. "service_down", "container_down", "missing_key", "quality", "deploy"
	Service     string   // service name if applicable
	FixFunc     func() error // built-in auto-fix, nil if manual only
}

// Result holds the diagnostic results.
type Result struct {
	Issues       []Issue
	ChecksPassed int
}

// RunChecks runs all diagnostic categories and returns results.
func RunChecks() *Result {
	r := &Result{}

	checkConnectivity(r)
	checkAPIKeys(r)
	checkContainers(r)
	checkDownloadClient(r)
	checkDiskSpace(r)
	checkMediaPaths(r)
	checkRootFolders(r)
	checkQualityConfig(r)
	checkIndexers(r)
	checkServiceWarnings(r)
	checkVPN(r)
	checkPermissions(r)
	checkHardlinks(r)
	checkCrossService(r)
	checkNewServices(r)

	return r
}

func checkConnectivity(r *Result) {
	fmt.Println(ui.Bold("  Service Connectivity"))
	fmt.Println(ui.Separator())

	// Probe all services across candidate hosts (localhost, global host, WSL gateway)
	probed := config.ProbeAll()

	for _, name := range config.AllServiceNames() {
		def, ok := config.GetServiceDef(name)
		if !ok || def.Port == 0 {
			continue
		}

		configured := config.IsConfigured(name)
		ss := probed[name]
		port := config.ServicePort(name)

		addr := fmt.Sprintf(":%d", port)
		if ss.Host != "" && ss.Host != "localhost" && ss.Host != "127.0.0.1" {
			addr = fmt.Sprintf("%s:%d", ss.Host, port)
		}
		rtLabel := "  " + ui.Dim(ss.Runtime.Label)

		if ss.Up {
			r.ChecksPassed++
			speed := ui.Ok(fmt.Sprintf("%dms", ss.LatencyMs))
			if ss.LatencyMs > 2000 {
				speed = ui.Warn(fmt.Sprintf("%dms (slow)", ss.LatencyMs))
				r.Issues = append(r.Issues, Issue{Description:
					fmt.Sprintf("SLOW SERVICE: %s responded in %dms (>2s). URL: http://%s:%d/. Check resource usage or network latency.",
						name, ss.LatencyMs, ss.Host, port),
				})
			}
			fmt.Printf("  %s %-15s %-12s %s%s\n", ui.Ok("✓"), name, ui.Dim(addr), speed, rtLabel)
		} else if configured {
			extra := tryDockerDiag(name, def.ContainerName, port)
			r.Issues = append(r.Issues, Issue{Description:
				fmt.Sprintf("UNREACHABLE: %s — tried %s. %s",
					name, formatCandidates(name, port), extra.fixHint),
			})
			statusExtra := ""
			if extra.short != "" {
				statusExtra = " " + ui.Dim("("+extra.short+")")
			}
			fmt.Printf("  %s %-15s %-12s %s%s%s\n", ui.Err("✗"), name, ui.Dim(addr), ui.Err("unreachable"), statusExtra, rtLabel)
		} else {
			fmt.Printf("  %s %-15s %-12s %s%s\n", ui.Dim("—"), name, ui.Dim(fmt.Sprintf(":%d", def.Port)), ui.Dim("not detected"), rtLabel)
		}
	}
}

// formatCandidates returns a human-readable list of hosts that were tried.
func formatCandidates(name string, port int) string {
	hosts := config.CandidateHosts(name)
	var parts []string
	for _, h := range hosts {
		parts = append(parts, fmt.Sprintf("http://%s:%d/", h, port))
	}
	return strings.Join(parts, ", ")
}

type diagInfo struct {
	short   string
	fixHint string
}

// tryDockerDiag attempts to get diagnostic info from Docker if available.
// Falls back to generic hints if Docker is not available.
func tryDockerDiag(name, container string, port int) diagInfo {
	// Try docker inspect (works if Docker is available and container exists)
	out, err := exec.Command("docker", "inspect", "-f", "{{.State.Status}}", container).Output()
	if err != nil {
		// Docker not available or container not found — give generic hint
		return diagInfo{
			fixHint: fmt.Sprintf("Check that %s is running and listening on port %d.", name, port),
		}
	}

	state := strings.TrimSpace(string(out))
	switch {
	case state == "running":
		return diagInfo{
			short:   "container up, port not responding",
			fixHint: fmt.Sprintf("Container '%s' is running but port %d not responding. Check logs: docker logs --tail 30 %s", container, port, container),
		}
	case state != "":
		return diagInfo{
			short:   state,
			fixHint: fmt.Sprintf("Container '%s' state: %s. Try: docker start %s", container, state, container),
		}
	default:
		return diagInfo{
			fixHint: fmt.Sprintf("Check that %s is running and listening on port %d.", name, port),
		}
	}
}

func checkAPIKeys(r *Result) {
	fmt.Println(ui.Bold("\n  API Keys"))
	fmt.Println(ui.Separator())

	for _, name := range config.AllServiceNames() {
		def, ok := config.GetServiceDef(name)
		if !ok || def.KeySource == "none" || !def.HasAPI {
			continue
		}

		configured := config.IsConfigured(name)
		key := keys.Get(name)
		if key != "" {
			r.ChecksPassed++
			masked := key[:4] + "…" + key[len(key)-4:]
			if len(key) <= 8 {
				masked = "****"
			}
			fmt.Printf("  %s %-15s %s\n", ui.Ok("✓"), name, ui.Dim(masked))
		} else if configured {
			host := config.ServiceHost(name)
			port := config.ServicePort(name)
			hint := fmt.Sprintf("Get the API key from the %s web UI (http://%s:%d/) under Settings.", name, host, port)
			r.Issues = append(r.Issues, Issue{Description: fmt.Sprintf("API KEY MISSING: %s — %s", name, hint)})
			fmt.Printf("  %s %-15s %s\n", ui.Err("✗"), name, ui.Err("not found"))
		}
		// Non-configured services without keys are silently skipped
	}
}

// checkContainers checks Docker container status if Docker is available.
func checkContainers(r *Result) {
	fmt.Println(ui.Bold("\n  Docker Containers"))
	fmt.Println(ui.Separator())

	// Build filter for all known container names
	var args []string
	args = append(args, "ps", "-a", "--format", "{{.Names}}\t{{.Status}}\t{{.Image}}")
	for _, name := range config.AllServiceNames() {
		container := config.ContainerName(name)
		args = append(args, "--filter", "name=^"+container+"$")
	}

	out, err := exec.Command("docker", args...).Output()
	if err != nil {
		fmt.Printf("  %s %s\n", ui.Dim("—"), ui.Dim("Docker not available (skipping container checks)"))
		return
	}

	lines := strings.TrimSpace(string(out))
	if lines == "" {
		fmt.Printf("  %s %s\n", ui.Dim("—"), ui.Dim("No managed containers found"))
		return
	}

	for _, line := range strings.Split(lines, "\n") {
		parts := strings.SplitN(line, "\t", 3)
		cname := "?"
		status := "?"
		image := "?"
		if len(parts) > 0 {
			cname = parts[0]
		}
		if len(parts) > 1 {
			status = parts[1]
		}
		if len(parts) > 2 {
			image = parts[2]
		}
		if strings.Contains(status, "Up") {
			r.ChecksPassed++
			fmt.Printf("  %s %-15s %s %s\n", ui.Ok("✓"), cname, ui.Ok(status), ui.Dim(image))
		} else {
			r.Issues = append(r.Issues, Issue{Description:
				fmt.Sprintf("CONTAINER DOWN: '%s' (image: %s) status: %s. Fix: docker start %s", cname, image, status, cname),
			})
			fmt.Printf("  %s %-15s %s %s\n", ui.Err("✗"), cname, ui.Err(status), ui.Dim(image))
		}
	}
}

func checkDownloadClient(r *Result) {
	fmt.Println(ui.Bold("\n  Download Client (qBittorrent)"))
	fmt.Println(ui.Separator())

	svc := config.Get().Services["qbittorrent"]

	// 1. Check qBittorrent reachability
	if !api.CheckReachable("qbittorrent") {
		r.Issues = append(r.Issues, Issue{Description:
			fmt.Sprintf("QBITTORRENT UNREACHABLE at http://%s:%d/. "+
				"Check that qBittorrent is running and WebUI is enabled. "+
				"If WebUI binds to 127.0.0.1, change it to 0.0.0.0 in Options → Web UI → IP address.",
				svc.Host, svc.Port),
		})
		fmt.Printf("  %s qBittorrent at %s:%d — %s\n", ui.Err("✗"), svc.Host, svc.Port, ui.Err("unreachable"))

		// Try to diagnose via config file for native/remote services
		rt := config.DetectRuntime("qbittorrent")
		if rt.Type == config.TypeNative || rt.Type == config.TypeRemote {
			checkQbitNativeConfig(r)
		}
		return
	}

	// 2. Get qBit version
	qc := qbit.New()
	ver, err := qc.Version()
	if err == nil {
		fmt.Printf("  %s qBittorrent %s at %s:%d\n", ui.Ok("✓"), ver, svc.Host, svc.Port)
		r.ChecksPassed++
	}

	// 3. Check preferences (bind address, save path)
	prefs, err := qc.Preferences()
	if err == nil {
		if prefs.WebUIAddress == "*" || prefs.WebUIAddress == "0.0.0.0" || prefs.WebUIAddress == "" {
			r.ChecksPassed++
			fmt.Printf("  %s WebUI bind: %s (accessible from network)\n", ui.Ok("✓"), prefs.WebUIAddress)
		} else if prefs.WebUIAddress == "127.0.0.1" || prefs.WebUIAddress == "localhost" {
			r.Issues = append(r.Issues, Issue{Description:
				fmt.Sprintf("QBITTORRENT BIND ADDRESS: WebUI bound to %s — not accessible from other machines. "+
					"Change to 0.0.0.0 in Options → Web UI → IP address.", prefs.WebUIAddress),
			})
			fmt.Printf("  %s WebUI bind: %s %s\n", ui.Warn("!"), prefs.WebUIAddress, ui.Warn("(localhost only — other services may not reach it)"))
		}

		// Just report save path — no hardcoded expectation.
		// The Download Pipeline check cross-validates paths against actual root folders.
		if prefs.SavePath != "" {
			r.ChecksPassed++
			fmt.Printf("  %s Save path: %s\n", ui.Ok("✓"), prefs.SavePath)
		} else {
			r.Issues = append(r.Issues, Issue{Description:
				"QBITTORRENT SAVE PATH: Not configured. Set in Options → Downloads → Default Save Path.",
			})
			fmt.Printf("  %s Save path: %s\n", ui.Err("✗"), ui.Err("not set"))
		}
	}

	// 4. List categories — cross-validation happens in Download Pipeline check
	cats, err := qc.Categories()
	if err == nil {
		if len(cats) > 0 {
			r.ChecksPassed++
			var catNames []string
			for name := range cats {
				catNames = append(catNames, name)
			}
			fmt.Printf("  %s Categories: %s\n", ui.Ok("✓"), strings.Join(catNames, ", "))
		} else {
			fmt.Printf("  %s %s\n", ui.Warn("!"), ui.Warn("No categories configured — downloads may land in wrong folder"))
		}
	}

	// 5. Check *Arr download client config points to qBit correctly
	for _, svcName := range []string{"radarr", "sonarr"} {
		if !api.CheckReachable(svcName) {
			continue
		}
		client := arr.New(svcName)
		clients, err := client.DownloadClients()
		if err != nil {
			continue
		}

		var found bool
		for _, dc := range clients {
			if dc.Implementation == "QBittorrent" {
				found = true
				host := fmt.Sprintf("%v", dc.GetField("host"))
				port := fmt.Sprintf("%v", dc.GetField("port"))

				// Check if the configured host:port actually resolves to qBit
				if dc.Enable {
					r.ChecksPassed++
					fmt.Printf("  %s [%s] download client → %s:%s\n", ui.Ok("✓"), svcName, host, port)
				} else {
					r.Issues = append(r.Issues, Issue{Description:
						fmt.Sprintf("DOWNLOAD CLIENT DISABLED: qBittorrent client in %s is disabled. Enable it in %s Settings → Download Clients.", svcName, svcName),
					})
					fmt.Printf("  %s [%s] download client → %s:%s %s\n", ui.Err("✗"), svcName, host, port, ui.Err("disabled"))
				}
				break
			}
		}
		if !found {
			r.Issues = append(r.Issues, Issue{Description:
				fmt.Sprintf("NO DOWNLOAD CLIENT: %s has no qBittorrent download client configured. Run admirarr setup or add manually in %s Settings → Download Clients.",
					svcName, svcName),
			})
			fmt.Printf("  %s [%s] %s\n", ui.Err("✗"), svcName, ui.Err("no qBittorrent client configured"))
		}
	}
}

// checkQbitNativeConfig reads qBittorrent config from native filesystem to diagnose issues.
func checkQbitNativeConfig(r *Result) {
	paths := qbitConfigPaths()
	for _, iniPath := range paths {
		data, err := os.ReadFile(iniPath)
		if err != nil {
			continue
		}

		lines := strings.Split(string(data), "\n")
		for _, line := range lines {
			line = strings.TrimSpace(line)
			if strings.HasPrefix(line, "WebUI\\Address=") || strings.HasPrefix(line, "WebUI\\Port=") ||
				strings.HasPrefix(line, "WebUI\\Enabled=") {
				parts := strings.SplitN(line, "=", 2)
				if len(parts) == 2 {
					key := strings.TrimPrefix(parts[0], "WebUI\\")
					val := parts[1]
					if key == "Address" && (val == "127.0.0.1" || val == "localhost") {
						fmt.Printf("  %s Config: %s — WebUI bound to %s (change to 0.0.0.0)\n",
							ui.Warn("!"), ui.Dim(iniPath), val)
					} else if key == "Enabled" && val == "false" {
						fmt.Printf("  %s Config: %s — WebUI is disabled\n",
							ui.Err("✗"), ui.Dim(iniPath))
					}
				}
			}
		}
		return // only check first user found
	}
}

// qbitConfigPaths returns candidate paths for qBittorrent config files.
func qbitConfigPaths() []string {
	home := os.Getenv("HOME")
	var paths []string

	// WSL: Windows paths
	if _, err := os.Stat("/mnt/c/Windows"); err == nil {
		entries, _ := os.ReadDir("/mnt/c/Users")
		for _, e := range entries {
			if !e.IsDir() || e.Name() == "Public" || e.Name() == "Default" || e.Name() == "Default User" || e.Name() == "All Users" {
				continue
			}
			paths = append(paths,
				fmt.Sprintf("/mnt/c/Users/%s/AppData/Roaming/qBittorrent/qBittorrent.ini", e.Name()),
				fmt.Sprintf("/mnt/c/Users/%s/AppData/Local/qBittorrent/qBittorrent.ini", e.Name()),
			)
		}
	}

	switch runtime.GOOS {
	case "darwin":
		paths = append(paths, filepath.Join(home, "Library", "Application Support", "qBittorrent", "qBittorrent.ini"))
	default:
		paths = append(paths,
			filepath.Join(home, ".config", "qBittorrent", "qBittorrent.ini"),
			filepath.Join(home, ".local", "share", "qBittorrent", "qBittorrent.ini"),
		)
	}

	return paths
}

// checkDiskSpace queries root folders from Radarr/Sonarr via API to find actual
// media paths, then checks disk space on each unique filesystem. Falls back to
// the configured data_path if no services are reachable.
func checkDiskSpace(r *Result) {
	fmt.Println(ui.Bold("\n  Disk Space"))
	fmt.Println(ui.Separator())

	// Collect unique paths from actual service root folders
	checked := make(map[string]bool)

	for _, svcName := range []string{"radarr", "sonarr"} {
		if !api.CheckReachable(svcName) {
			continue
		}
		roots, err := arr.New(svcName).RootFolders()
		if err != nil {
			continue
		}
		for _, root := range roots {
			// Root folders report their own free space — use it directly
			if root.FreeSpace > 0 && !checked[root.Path] {
				checked[root.Path] = true
				label := fmt.Sprintf("[%s] %s", svcName, root.Path)
				freeGB := float64(root.FreeSpace) / (1024 * 1024 * 1024)
				if freeGB < 10 {
					r.Issues = append(r.Issues, Issue{Description:
						fmt.Sprintf("DISK LOW: %s has only %s free.", label, ui.FmtSize(root.FreeSpace)),
					})
					fmt.Printf("  %s %s  %s free\n", ui.Warn("!"), label, ui.Warn(ui.FmtSize(root.FreeSpace)))
				} else {
					r.ChecksPassed++
					fmt.Printf("  %s %s  %s free\n", ui.Ok("✓"), label, ui.FmtSize(root.FreeSpace))
				}
			}
		}
	}

	// Also check qBittorrent save path if reachable
	if api.CheckReachable("qbittorrent") {
		prefs, err := qbit.New().Preferences()
		if err == nil && prefs.SavePath != "" && !checked[prefs.SavePath] {
			checked[prefs.SavePath] = true
			total, free, err := statfs(prefs.SavePath)
			if err == nil {
				checkDiskPath(r, "[qbittorrent] "+prefs.SavePath, total, free)
			}
		}
	}

	// Fallback: check local data_path if nothing was discovered
	if len(checked) == 0 {
		dataPath := config.DataPath()
		total, free, err := statfs(dataPath)
		if err != nil {
			fmt.Printf("  %s No media paths discovered (services down?) and %s not accessible\n",
				ui.Dim("—"), dataPath)
			return
		}
		checkDiskPath(r, dataPath, total, free)
	}
}

func checkDiskPath(r *Result, label string, total, free int64) {
	pctUsed := float64(total-free) / float64(total) * 100
	if pctUsed > 95 {
		r.Issues = append(r.Issues, Issue{Description:
			fmt.Sprintf("DISK CRITICAL: %s is %.0f%% full, only %s free of %s.", label, pctUsed, ui.FmtSize(free), ui.FmtSize(total)),
		})
		fmt.Printf("  %s %s  %s — %s free / %s\n", ui.Err("✗"), label, ui.Err(fmt.Sprintf("%.0f%% used", pctUsed)), ui.FmtSize(free), ui.FmtSize(total))
	} else if pctUsed > 85 {
		r.Issues = append(r.Issues, Issue{Description:
			fmt.Sprintf("DISK LOW: %s is %.0f%% full, %s free of %s.", label, pctUsed, ui.FmtSize(free), ui.FmtSize(total)),
		})
		fmt.Printf("  %s %s  %s — %s free / %s\n", ui.Warn("!"), label, ui.Warn(fmt.Sprintf("%.0f%% used", pctUsed)), ui.FmtSize(free), ui.FmtSize(total))
	} else {
		r.ChecksPassed++
		fmt.Printf("  %s %s  %s — %s free / %s\n", ui.Ok("✓"), label, ui.Ok(fmt.Sprintf("%.0f%% used", pctUsed)), ui.FmtSize(free), ui.FmtSize(total))
	}
}

// checkMediaPaths validates the download pipeline wiring by cross-checking
// actual configurations from each service API:
//   - Radarr/Sonarr root folders (where media ends up)
//   - Radarr/Sonarr download client config (how they talk to qBit)
//   - qBittorrent categories + save paths (where downloads land)
//
// No hardcoded paths — everything is discovered from the APIs.
func checkMediaPaths(r *Result) {
	fmt.Println(ui.Bold("\n  Download Pipeline"))
	fmt.Println(ui.Separator())

	qbitReachable := api.CheckReachable("qbittorrent")
	var qbitPrefs *qbit.Preferences
	var qbitCats map[string]qbit.Category
	if qbitReachable {
		qc := qbit.New()
		qbitPrefs, _ = qc.Preferences()
		qbitCats, _ = qc.Categories()
	}

	for _, item := range []struct {
		svc           string
		categoryField string
		label         string
	}{
		{"radarr", "movieCategory", "Movies"},
		{"sonarr", "tvCategory", "TV"},
	} {
		if !api.CheckReachable(item.svc) {
			fmt.Printf("  %s [%s] %s\n", ui.Dim("—"), item.svc, ui.Dim("not reachable — skipping pipeline check"))
			continue
		}

		client := arr.New(item.svc)

		// 1. Get root folders from service
		roots, err := client.RootFolders()
		if err != nil || len(roots) == 0 {
			r.Issues = append(r.Issues, Issue{Description:
				fmt.Sprintf("NO ROOT FOLDER: %s has no root folders configured. Add one in %s Settings → Media Management.", item.svc, item.svc),
			})
			fmt.Printf("  %s [%s] %s\n", ui.Err("✗"), item.svc, ui.Err("no root folder"))
			continue
		}

		for _, root := range roots {
			if root.Accessible {
				fmt.Printf("  %s [%s] root folder: %s\n", ui.Ok("✓"), item.svc, root.Path)
				r.ChecksPassed++
			} else {
				r.Issues = append(r.Issues, Issue{Description:
					fmt.Sprintf("ROOT FOLDER INACCESSIBLE: %s root folder '%s' is not accessible. Check volume mounts or permissions.", item.svc, root.Path),
				})
				fmt.Printf("  %s [%s] root folder: %s %s\n", ui.Err("✗"), item.svc, root.Path, ui.Err("inaccessible"))
			}
		}

		// 2. Get download client config from service
		dcs, err := client.DownloadClients()
		if err != nil {
			continue
		}

		var qbitDC *arr.DownloadClient
		for i := range dcs {
			if dcs[i].Implementation == "QBittorrent" {
				qbitDC = &dcs[i]
				break
			}
		}

		if qbitDC == nil {
			r.Issues = append(r.Issues, Issue{Description:
				fmt.Sprintf("NO DOWNLOAD CLIENT: %s has no qBittorrent client. Add in Settings → Download Clients.", item.svc),
			})
			fmt.Printf("  %s [%s] %s\n", ui.Err("✗"), item.svc, ui.Err("no qBittorrent download client"))
			continue
		}

		dcHost := fmt.Sprintf("%v", qbitDC.GetField("host"))
		dcPort := fmt.Sprintf("%v", qbitDC.GetField("port"))
		dcCategory := ""
		if v := qbitDC.GetField(item.categoryField); v != nil {
			dcCategory = fmt.Sprintf("%v", v)
		}

		if !qbitDC.Enable {
			r.Issues = append(r.Issues, Issue{Description:
				fmt.Sprintf("DOWNLOAD CLIENT DISABLED: %s qBittorrent client is disabled.", item.svc),
			})
			fmt.Printf("  %s [%s] download client: %s:%s %s\n", ui.Err("✗"), item.svc, dcHost, dcPort, ui.Err("disabled"))
			continue
		}

		fmt.Printf("  %s [%s] download client: %s:%s (category: %s)\n",
			ui.Ok("✓"), item.svc, dcHost, dcPort, dcCategory)
		r.ChecksPassed++

		// 3. Cross-validate: does the qBit category exist and point somewhere sensible?
		if qbitReachable && qbitCats != nil && dcCategory != "" {
			if cat, ok := qbitCats[dcCategory]; ok {
				fmt.Printf("  %s [%s] qBit category '%s' → %s\n", ui.Ok("✓"), item.svc, dcCategory, cat.SavePath)
				r.ChecksPassed++
			} else {
				r.Issues = append(r.Issues, Issue{Description:
					fmt.Sprintf("CATEGORY MISSING IN QBIT: %s expects category '%s' but it doesn't exist in qBittorrent. Run admirarr setup to create it.", item.svc, dcCategory),
				})
				fmt.Printf("  %s [%s] qBit category '%s' %s\n", ui.Err("✗"), item.svc, dcCategory, ui.Err("not found in qBittorrent"))
			}
		}
	}

	// Show qBit default save path for reference
	if qbitPrefs != nil {
		fmt.Printf("  %s qBittorrent default save path: %s\n", ui.Dim("ℹ"), qbitPrefs.SavePath)
	}
}

// checkRootFolders is now handled by checkMediaPaths which cross-validates
// root folders against the full download pipeline. Kept as a no-op for
// backward compatibility with any external callers.
func checkRootFolders(r *Result) {
	// Root folder checks are now part of checkMediaPaths (Download Pipeline)
}

// checkQualityConfig verifies that quality profiles and custom formats are
// configured in *Arr services. Detects Recyclarr and reports its status.
func checkQualityConfig(r *Result) {
	fmt.Println(ui.Bold("\n  Quality & Custom Formats"))
	fmt.Println(ui.Separator())

	// Detect Recyclarr
	rt := recyclarr.Detect()
	switch rt.Method {
	case "native":
		r.ChecksPassed++
		fmt.Printf("  %s Recyclarr installed: %s %s\n", ui.Ok("✓"), rt.Path, ui.Dim(rt.Version))
	case "docker":
		r.ChecksPassed++
		fmt.Printf("  %s Recyclarr (Docker): %s %s\n", ui.Ok("✓"), rt.Path, ui.Dim(rt.Version))
	default:
		r.Issues = append(r.Issues, Issue{
			Description: "RECYCLARR NOT INSTALLED: Recyclarr syncs TRaSH Guides quality profiles and custom formats to Radarr/Sonarr",
			Category:    "deploy",
			Service:     "recyclarr",
		})
		fmt.Printf("  %s Recyclarr: %s\n", ui.Warn("!"), ui.Warn("not installed (run 'admirarr doctor --fix' to deploy)"))
	}

	// Verify quality profiles via APIs (works regardless of Recyclarr)
	results := recyclarr.Verify("radarr", "sonarr")
	for _, v := range results {
		if len(v.Issues) > 0 {
			for _, issue := range v.Issues {
				fmt.Printf("  %s [%s] %s\n", ui.Err("✗"), v.Service, issue)
			}
			continue
		}

		profileInfo := fmt.Sprintf("%d profiles", v.QualityProfiles)
		formatInfo := fmt.Sprintf("%d custom formats", v.CustomFormats)

		if v.CustomFormats > 0 {
			r.ChecksPassed++
			fmt.Printf("  %s [%s] %s, %s\n", ui.Ok("✓"), v.Service, profileInfo, formatInfo)
		} else {
			r.Issues = append(r.Issues, Issue{
				Description: fmt.Sprintf("NO CUSTOM FORMATS: [%s] %s, %s — consider running Recyclarr to apply TRaSH Guides", v.Service, profileInfo, formatInfo),
				Category:    "quality",
				Service:     v.Service,
			})
			fmt.Printf("  %s [%s] %s, %s %s\n", ui.Warn("!"), v.Service, profileInfo, formatInfo,
				ui.Dim("(run 'admirarr doctor --fix' or 'admirarr recyclarr sync')"))
		}
	}
}

func checkIndexers(r *Result) {
	fmt.Println(ui.Bold("\n  Indexers"))
	fmt.Println(ui.Separator())

	client := arr.New("prowlarr")
	indexers, err := client.Indexers()
	if err != nil {
		fmt.Printf("  %s %s\n", ui.Dim("—"), ui.Dim("Cannot check (Prowlarr down)"))
		return
	}

	statuses, _ := client.IndexerStatuses()

	failedMap := make(map[int]string)
	for _, s := range statuses {
		if s.MostRecentFailure != "" {
			failedMap[s.IndexerID] = s.DisabledTill
		}
	}

	var healthy, failing, disabled []string
	for _, idx := range indexers {
		if !idx.Enable {
			disabled = append(disabled, idx.Name)
		} else if _, ok := failedMap[idx.ID]; ok {
			failing = append(failing, idx.Name)
		} else {
			healthy = append(healthy, idx.Name)
		}
	}

	if len(healthy) > 0 {
		r.ChecksPassed++
		fmt.Printf("  %s %d indexer(s) healthy: %s\n", ui.Ok("✓"), len(healthy), strings.Join(healthy, ", "))
	}
	if len(failing) > 0 {
		r.Issues = append(r.Issues, Issue{Description:
			fmt.Sprintf("INDEXERS FAILING: %d indexer(s) failing: %s. Check Prowlarr.", len(failing), strings.Join(failing, ", ")),
		})
		fmt.Printf("  %s %d failing: %s\n", ui.Err("✗"), len(failing), strings.Join(failing, ", "))
	}
	if len(disabled) > 0 {
		fmt.Printf("  %s %d disabled: %s\n", ui.Dim("—"), len(disabled), strings.Join(disabled, ", "))
	}
}

func checkServiceWarnings(r *Result) {
	fmt.Println(ui.Bold("\n  Service Warnings"))
	fmt.Println(ui.Separator())

	// Check health endpoints on all *arr services that have an API version
	found := false
	for _, name := range config.AllServiceNames() {
		ver := config.ServiceAPIVer(name)
		if ver == "" {
			continue
		}
		items, err := arr.New(name).Health()
		if err == nil && len(items) > 0 {
			for _, item := range items {
				found = true
				level := ui.Warn("WARN")
				if item.Type == "error" {
					level = ui.Err("ERROR")
				}
				fmt.Printf("  %s %s %s\n", level, ui.Dim("["+name+"]"), item.Message)
				if item.WikiURL != "" {
					fmt.Printf("         %s\n", ui.Dim(item.WikiURL))
				}
				r.Issues = append(r.Issues, Issue{Description:
					fmt.Sprintf("HEALTH WARNING [%s] (%s): %s",
						name, item.Type, item.Message),
				})
			}
		}
	}
	if !found {
		r.ChecksPassed++
		fmt.Printf("  %s No warnings from *Arr services\n", ui.Ok("✓"))
	}
}
