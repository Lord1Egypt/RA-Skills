package doctor

import (
	"fmt"
	"os"
	"os/exec"
	"strings"
	"time"

	"github.com/charmbracelet/huh"
	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/deploy"
	"github.com/maxtechera/admirarr/internal/recyclarr"
	"github.com/maxtechera/admirarr/internal/ui"
)

type agentInfo struct {
	Cmd       string
	Name      string
	Flag      string
	ToolsFlag string
	Version   string
}

// Fix runs the fix wizard: built-in fixes first, then AI agent for the rest.
func Fix(issues []Issue) {
	fmt.Printf("\n  %s\n", ui.Dim("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
	fmt.Printf("  %s %s\n\n", ui.GoldText("⚓"), ui.Bold("Fix Wizard"))

	// Phase 1: Run built-in fixes
	var remaining []Issue
	fixed := 0

	for _, issue := range issues {
		if issue.FixFunc != nil {
			fmt.Printf("  %s %s\n", ui.GoldText("⟳"), issue.Description)
			if err := issue.FixFunc(); err != nil {
				fmt.Printf("  %s Fix failed: %v\n\n", ui.Err("✗"), err)
				remaining = append(remaining, issue)
			} else {
				fmt.Printf("  %s Fixed\n\n", ui.Ok("✓"))
				fixed++
			}
			continue
		}

		// Try category-based built-in fixes
		if tryBuiltinFix(issue) {
			fixed++
		} else {
			remaining = append(remaining, issue)
		}
	}

	if fixed > 0 {
		fmt.Printf("  %s\n", ui.Dim("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
		fmt.Printf("  %s auto-fixed\n\n", ui.Ok(fmt.Sprintf("%d issue(s)", fixed)))
	}

	if len(remaining) == 0 {
		fmt.Printf("  %s All issues resolved. Run %s to verify.\n\n",
			ui.Ok("✓"), ui.GoldText("admirarr doctor"))
		return
	}

	// Phase 2: Offer AI agent for remaining issues
	fmt.Printf("  %s remaining that need manual attention or AI assistance:\n\n",
		ui.Warn(fmt.Sprintf("%d issue(s)", len(remaining))))
	for i, issue := range remaining {
		fmt.Printf("  %s %s\n", ui.Dim(fmt.Sprintf("%d.", i+1)), issue.Description)
	}
	fmt.Println()

	agents := detectAgents()
	if len(agents) == 0 {
		fmt.Printf("  %s\n", ui.Dim("Install an AI agent CLI to auto-fix remaining issues:"))
		fmt.Printf("    %s  npm install -g @anthropic-ai/claude-code\n", ui.Dim("Claude Code:"))
		fmt.Printf("    %s     go install github.com/opencode-ai/opencode@latest\n", ui.Dim("OpenCode:"))
		fmt.Printf("\n  %s\n\n", ui.Dim("Or fix manually using the hints above."))
		return
	}

	runAgentFix(agents, remaining)
}

// tryBuiltinFix attempts to fix an issue using built-in logic based on the
// issue description pattern. Returns true if fixed.
func tryBuiltinFix(issue Issue) bool {
	desc := issue.Description

	// Gluetun unhealthy / VPN disconnected → check if it's a credentials issue
	if strings.Contains(desc, "GLUETUN") || strings.Contains(desc, "gluetun") ||
		(strings.Contains(desc, "VPN") && !strings.Contains(desc, "ROUTING")) {
		out, err := exec.Command("docker", "logs", "--tail", "20", config.ContainerName("gluetun")).CombinedOutput()
		if err == nil && strings.Contains(string(out), "private key is not set") {
			fmt.Printf("  %s Gluetun needs VPN credentials (Wireguard private key not set).\n", ui.Warn("!"))
			fmt.Printf("    Configure VPN credentials in your docker-compose .env file:\n")
			fmt.Printf("    %s\n", ui.Dim("WIREGUARD_PRIVATE_KEY=<your-key>"))
			fmt.Printf("    %s\n\n", ui.Dim("WIREGUARD_ADDRESSES=<your-address>"))
			return false // Can't auto-fix — needs user credentials
		}
	}

	// qBittorrent depends on gluetun network — check if gluetun is the problem
	if strings.Contains(desc, "qbittorrent") || strings.Contains(desc, "QBITTORRENT") {
		gluetunHealth, _ := exec.Command("docker", "inspect", "-f", "{{.State.Health.Status}}", config.ContainerName("gluetun")).Output()
		if strings.TrimSpace(string(gluetunHealth)) != "healthy" {
			qbitNet, _ := exec.Command("docker", "inspect", "-f", "{{.HostConfig.NetworkMode}}", config.ContainerName("qbittorrent")).Output()
			if strings.Contains(string(qbitNet), "gluetun") || strings.Contains(string(qbitNet), "container:") {
				fmt.Printf("  %s qBittorrent depends on Gluetun network (Gluetun is unhealthy).\n", ui.Warn("!"))
				fmt.Printf("    Fix Gluetun VPN credentials first, then qBittorrent will start automatically.\n\n")
				return false
			}
		}
	}

	// Container down → docker start
	if strings.HasPrefix(desc, "CONTAINER DOWN:") {
		container := extractContainerName(desc)
		if container != "" {
			fmt.Printf("  %s Starting container %s…\n", ui.GoldText("⟳"), container)
			cmd := exec.Command("docker", "start", container)
			if out, err := cmd.CombinedOutput(); err != nil {
				fmt.Printf("  %s docker start %s failed: %s\n\n", ui.Err("✗"), container, strings.TrimSpace(string(out)))
				return false
			}
			// Wait for it to come up
			time.Sleep(3 * time.Second)
			fmt.Printf("  %s Container %s started\n\n", ui.Ok("✓"), container)
			return true
		}
	}

	// Service unreachable with Docker container → try docker start
	if strings.HasPrefix(desc, "UNREACHABLE:") && strings.Contains(desc, "docker start") {
		// Extract container name from "Try: docker start <container>"
		if idx := strings.Index(desc, "docker start "); idx >= 0 {
			container := strings.TrimSpace(desc[idx+len("docker start "):])
			fmt.Printf("  %s Starting container %s…\n", ui.GoldText("⟳"), container)
			if err := exec.Command("docker", "start", container).Run(); err == nil {
				time.Sleep(3 * time.Second)
				fmt.Printf("  %s Container %s started\n\n", ui.Ok("✓"), container)
				return true
			}
		}
	}

	// Recyclarr not installed → deploy via Docker
	if strings.Contains(desc, "Recyclarr") && strings.Contains(desc, "not installed") {
		return deployService("recyclarr")
	}

	// Missing service that can be deployed
	if issue.Category == "deploy" && issue.Service != "" {
		return deployService(issue.Service)
	}

	// Quality issues → run recyclarr sync if available
	if strings.Contains(desc, "consider running Recyclarr") || issue.Category == "quality" {
		rt := recyclarr.Detect()
		if rt.Method == "none" {
			// Deploy recyclarr first
			if deployService("recyclarr") {
				rt = recyclarr.Detect()
			}
		}
		if rt.Method != "none" {
			fmt.Printf("  %s Running Recyclarr sync…\n", ui.GoldText("⟳"))
			output, err := recyclarr.Sync(rt, "")
			if err != nil {
				lines := strings.Split(strings.TrimSpace(output), "\n")
				if len(lines) > 3 {
					lines = lines[len(lines)-3:]
				}
				for _, line := range lines {
					fmt.Printf("    %s\n", ui.Dim(line))
				}
				fmt.Printf("  %s Recyclarr sync failed: %v\n\n", ui.Err("✗"), err)
				return false
			}
			fmt.Printf("  %s Recyclarr sync complete\n\n", ui.Ok("✓"))
			return true
		}
	}

	// Media path missing → mkdir -p
	if strings.HasPrefix(desc, "MEDIA PATH MISSING:") || strings.HasPrefix(desc, "ROOT FOLDER INACCESSIBLE:") {
		// Extract path from description if possible
		if idx := strings.Index(desc, "'/"); idx >= 0 {
			end := strings.Index(desc[idx+1:], "'")
			if end > 0 {
				path := desc[idx+1 : idx+1+end]
				fmt.Printf("  %s Creating directory %s…\n", ui.GoldText("⟳"), path)
				if err := os.MkdirAll(path, 0755); err != nil {
					fmt.Printf("  %s mkdir failed: %v\n\n", ui.Err("✗"), err)
					return false
				}
				fmt.Printf("  %s Created %s\n\n", ui.Ok("✓"), path)
				return true
			}
		}
	}

	// Directory structure missing → create dirs
	if strings.HasPrefix(desc, "DIRECTORY STRUCTURE:") {
		dataPath := config.DataPath()
		dirs := []string{
			"torrents/movies", "torrents/tv", "torrents/music", "torrents/books",
			"usenet/movies", "usenet/tv", "usenet/music", "usenet/books",
			"media", "media/movies", "media/tv", "media/music", "media/books",
		}
		created := 0
		for _, d := range dirs {
			p := dataPath + "/" + d
			if _, err := os.Stat(p); os.IsNotExist(err) {
				if err := os.MkdirAll(p, 0755); err != nil {
					// Try via Docker if permission denied
					exec.Command("docker", "run", "--rm", "-v", dataPath+":/data", "alpine",
						"mkdir", "-p", "/data/"+d).Run()
				}
				created++
			}
		}
		if created > 0 {
			fmt.Printf("  %s Created %d directories under %s\n\n", ui.Ok("✓"), created, dataPath)
			return true
		}
	}

	// Failing indexer → delete and re-add
	if strings.HasPrefix(desc, "INDEXERS FAILING:") {
		return fixFailingIndexers(desc)
	}

	// EZTV / indexer health warnings → skip (handled by INDEXERS FAILING fix above)
	if strings.HasPrefix(desc, "HEALTH WARNING") && strings.Contains(desc, "Indexers unavailable due to failures") {
		fmt.Printf("  %s Health warning will clear after indexer fix or next sync\n\n", ui.Dim("—"))
		return true // Mark as handled — it's a consequence of the indexer fix
	}

	// Bazarr not connected → provide URL and instructions
	if strings.HasPrefix(desc, "BAZARR:") && strings.Contains(desc, "Not connected") {
		svc := config.Get().Services["bazarr"]
		fmt.Printf("  %s Bazarr wiring requires manual configuration:\n", ui.Warn("!"))
		fmt.Printf("    Open http://%s:%d/settings\n", svc.Host, svc.Port)
		if strings.Contains(desc, "Radarr") {
			fmt.Printf("    → Radarr tab: enter Radarr URL and API key\n")
		}
		if strings.Contains(desc, "Sonarr") {
			fmt.Printf("    → Sonarr tab: enter Sonarr URL and API key\n")
		}
		fmt.Println()
		return false
	}

	// Seerr not initialized → provide URL
	if strings.Contains(desc, "SEERR") && strings.Contains(desc, "Not initialized") {
		svc := config.Get().Services["seerr"]
		fmt.Printf("  %s Seerr needs initial setup at http://%s:%d/\n\n", ui.Warn("!"), svc.Host, svc.Port)
		return false
	}

	// Jellyfin API key missing → provide instructions
	if strings.Contains(desc, "API KEY MISSING") && strings.Contains(desc, "jellyfin") {
		svc := config.Get().Services["jellyfin"]
		fmt.Printf("  %s Jellyfin API key: open http://%s:%d/ → Dashboard → API Keys → Create\n", ui.Warn("!"), svc.Host, svc.Port)
		fmt.Printf("    Then add to config: admirarr setup or edit ~/.config/admirarr/config.yaml\n\n")
		return false
	}

	// VPN routing issues → informational
	if strings.Contains(desc, "VPN ROUTING") {
		fmt.Printf("  %s VPN routing will be fixed once Gluetun is healthy\n\n", ui.Dim("—"))
		return true
	}

	return false
}

// fixFailingIndexers deletes and re-adds failing indexers in Prowlarr.
func fixFailingIndexers(desc string) bool {
	client := arr.New("prowlarr")
	indexers, err := client.Indexers()
	if err != nil {
		fmt.Printf("  %s Cannot fetch indexers: %v\n\n", ui.Err("✗"), err)
		return false
	}

	statuses, _ := client.IndexerStatuses()
	failedIDs := make(map[int]bool)
	for _, s := range statuses {
		if s.MostRecentFailure != "" {
			failedIDs[s.IndexerID] = true
		}
	}

	fixed := 0
	for _, idx := range indexers {
		if !failedIDs[idx.ID] {
			continue
		}

		// Get full indexer config
		full, err := client.GetIndexerByID(idx.ID)
		if err != nil {
			fmt.Printf("  %s Cannot get indexer %s config: %v\n", ui.Err("✗"), idx.Name, err)
			continue
		}

		// Delete the failing indexer
		fmt.Printf("  %s Re-adding failing indexer: %s\n", ui.GoldText("⟳"), idx.Name)
		if err := client.DeleteIndexer(idx.ID); err != nil {
			fmt.Printf("  %s Cannot delete indexer %s: %v\n", ui.Err("✗"), idx.Name, err)
			continue
		}

		// Remove ID so Prowlarr creates a new one
		delete(full, "id")

		// Re-add
		_, err = client.AddIndexer(full)
		if err != nil {
			fmt.Printf("  %s Re-add indexer %s failed: %v\n", ui.Err("✗"), idx.Name, err)
			continue
		}
		fmt.Printf("  %s Re-added %s\n", ui.Ok("✓"), idx.Name)
		fixed++
	}

	if fixed > 0 {
		fmt.Println()
		return true
	}
	return false
}

// deployService deploys a service via Docker using the deploy package.
func deployService(service string) bool {
	fmt.Printf("  %s Deploying %s via Docker…\n", ui.GoldText("⟳"), service)
	result := deploy.Service(service)
	if result.Error != nil {
		fmt.Printf("  %s Deploy failed: %v\n\n", ui.Err("✗"), result.Error)
		return false
	}
	fmt.Printf("  %s %s deployed (container: %s)\n\n", ui.Ok("✓"), service, result.Container)
	return true
}

// extractContainerName pulls the container name from a CONTAINER DOWN description.
func extractContainerName(desc string) string {
	// Format: "CONTAINER DOWN: 'name' ..."
	start := strings.Index(desc, "'")
	if start < 0 {
		return ""
	}
	end := strings.Index(desc[start+1:], "'")
	if end < 0 {
		return ""
	}
	return desc[start+1 : start+1+end]
}

func runAgentFix(agents []agentInfo, issues []Issue) {
	// Select agent
	var agent agentInfo
	if len(agents) == 1 {
		agent = agents[0]
		fmt.Printf("  Using %s %s\n", ui.Bold(agent.Name), ui.Dim(agent.Version))
	} else {
		options := make([]huh.Option[int], len(agents))
		for i, a := range agents {
			options[i] = huh.NewOption(fmt.Sprintf("%s  %s", a.Name, ui.Dim(a.Version)), i)
		}
		var selected int
		form := huh.NewForm(
			huh.NewGroup(
				huh.NewSelect[int]().
					Title("Select AI agent for remaining fixes").
					Options(options...).
					Value(&selected),
			),
		)
		if err := form.Run(); err != nil {
			return
		}
		agent = agents[selected]
	}
	fmt.Printf("\n  %s Selected: %s\n\n", ui.Ok("✓"), ui.Bold(agent.Name))

	// Build the prompt
	issueList := make([]string, len(issues))
	for i, iss := range issues {
		issueList[i] = fmt.Sprintf("  %d. %s", i+1, iss.Description)
	}

	dataPath := config.DataPath()

	var serviceList []string
	for _, name := range config.AllServiceNames() {
		def, ok := config.GetServiceDef(name)
		if !ok || def.Port == 0 {
			continue
		}
		serviceList = append(serviceList, fmt.Sprintf("  - %s (:%d, container: %s)", name, def.Port, def.ContainerName))
	}

	prompt := fmt.Sprintf(`You are the admirarr doctor fix wizard for a *Arr media server stack.

ENVIRONMENT:
- Data path: %s
- Known services:
%s

REMAINING ISSUES (built-in fixes already attempted):
%s

FIX INSTRUCTIONS:
- Service unreachable: check if it's running (docker ps, systemctl status), try restarting, verify with curl
- API key not found: guide user to Settings > General in the service web UI
- Media path missing: mkdir -p <path>
- Disk space: report usage, suggest cleanup — DO NOT delete anything
- Docker container down: docker start <container>
- Indexer failures: check FlareSolverr, report Prowlarr status
- *Arr health warnings: explain and provide fix commands
- Root folder inaccessible: check volume mounts and permissions
- Missing service: deploy via docker compose or suggest admirarr setup

For each issue print:
  Fixing: <description>
  Action: <command or step>
  Result: <outcome>

Fix what you can automatically. For manual steps, provide exact commands.`,
		dataPath, strings.Join(serviceList, "\n"), strings.Join(issueList, "\n"))

	// Confirm
	var action string
	form := huh.NewForm(
		huh.NewGroup(
			huh.NewSelect[string]().
				Title("Run AI fix for remaining issues?").
				Options(
					huh.NewOption("Yes — run the fix", "yes"),
					huh.NewOption("Cancel", "no"),
				).
				Value(&action),
		),
	)
	if err := form.Run(); err != nil || action == "no" {
		fmt.Printf("  %s\n", ui.Dim("Cancelled."))
		return
	}

	// Stream the fix
	fmt.Printf("  %s\n", ui.Dim("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
	fmt.Printf("  %s Streaming fixes via %s...\n\n", ui.GoldText("⚓"), ui.Bold(agent.Name))

	cmdParts := []string{agent.Cmd, agent.Flag, prompt}
	if agent.ToolsFlag != "" {
		cmdParts = append(cmdParts, strings.Fields(agent.ToolsFlag)...)
	}

	proc := exec.Command(cmdParts[0], cmdParts[1:]...)

	// Clear CLAUDE env vars to avoid parent session detection
	env := os.Environ()
	filteredEnv := make([]string, 0, len(env))
	for _, e := range env {
		if !strings.HasPrefix(e, "CLAUDECODE=") && !strings.HasPrefix(e, "CLAUDE_") {
			filteredEnv = append(filteredEnv, e)
		}
	}
	proc.Env = filteredEnv
	proc.Stdout = os.Stdout
	proc.Stderr = os.Stderr
	proc.Stdin = os.Stdin

	if err := proc.Run(); err != nil {
		fmt.Printf("\n  %s\n", ui.Err(fmt.Sprintf("Agent exited with error: %v", err)))
	}

	fmt.Printf("\n  %s\n", ui.Dim("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
	fmt.Printf("  %s %s %s\n", ui.Dim("Re-run"), ui.GoldText("admirarr doctor"), ui.Dim("to verify fixes."))
}

func detectAgents() []agentInfo {
	agentDefs := []struct {
		Cmd       string
		Name      string
		Flag      string
		ToolsFlag string
	}{
		{"claude", "Claude Code", "-p", "--allowedTools Bash"},
		{"opencode", "OpenCode", "-p", ""},
		{"aider", "Aider", "--message", ""},
		{"goose", "Goose", "-m", ""},
	}

	var found []agentInfo
	for _, def := range agentDefs {
		out, err := exec.Command(def.Cmd, "--version").Output()
		if err != nil {
			continue
		}
		ver := strings.TrimSpace(strings.Split(string(out), "\n")[0])
		if len(ver) > 40 {
			ver = ver[:40]
		}
		found = append(found, agentInfo{
			Cmd:       def.Cmd,
			Name:      def.Name,
			Flag:      def.Flag,
			ToolsFlag: def.ToolsFlag,
			Version:   ver,
		})
	}
	return found
}
