package setup

import (
	"fmt"
	"strings"

	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/ui"
)

// SetupState accumulates validated configuration across all phases.
type SetupState struct {
	DataPath         string
	ComposeDir       string
	ConfigDir        string
	Timezone         string
	VPNProvider      string
	VPNType          string
	RemoteHost      string // Remote host IP for non-Docker services (auto-detected on WSL)
	SelectedServices []string
	Services         map[string]*ServiceState
	Keys             map[string]string
	// ManualKeys tracks keys the user entered manually (need persisting).
	ManualKeys map[string]string
	// VPNCreds holds provider-specific VPN credentials for Gluetun.
	VPNCreds map[string]string
	// Indexers holds the desired indexer set (populated during Phase 7).
	Indexers map[string]config.IndexerConfig
	// JellyfinUser and JellyfinPassword store credentials set during Jellyfin init.
	JellyfinUser     string
	JellyfinPassword string
	// SeerrInitialized is set to true when initSeerr() completes successfully.
	SeerrInitialized bool
	// AutoMode skips interactive prompts, using detected/configured defaults.
	AutoMode bool
}

// ServiceState tracks the detected state of a single service.
type ServiceState struct {
	Detected  bool
	Reachable bool
	IsDocker  bool
	Host      string
	Port      int
	APIKey    string
}

// InternalURL returns the inter-service URL for a service.
// Docker services use container names; remote services use the remote host IP;
// native services use localhost.
func (s *SetupState) InternalURL(service string) string {
	svc := s.Services[service]
	def, _ := config.GetServiceDef(service)
	port := def.Port
	if svc != nil && svc.Port > 0 {
		port = svc.Port
	}
	if svc != nil && svc.IsDocker {
		return fmt.Sprintf("http://%s:%d", config.ContainerName(service), port)
	}
	// Remote services (native on another machine, e.g., Windows host via WSL)
	if svc != nil && svc.Host != "" && svc.Host != "localhost" && svc.Host != "127.0.0.1" {
		return fmt.Sprintf("http://%s:%d", svc.Host, port)
	}
	if s.RemoteHost != "" && svc != nil && !svc.IsDocker {
		return fmt.Sprintf("http://%s:%d", s.RemoteHost, port)
	}
	return fmt.Sprintf("http://localhost:%d", port)
}

// StepResult tracks what happened in each phase.
type StepResult struct {
	Name    string
	Passed  int
	Fixed   int
	Skipped int
	Errors  []string
}

func (r *StepResult) pass()                { r.Passed++ }
func (r *StepResult) fix()                 { r.Fixed++ }
func (r *StepResult) skip()                { r.Skipped++ }
func (r *StepResult) err(msg string)       { r.Errors = append(r.Errors, msg) }
func (r *StepResult) errf(f string, a ...interface{}) {
	r.Errors = append(r.Errors, fmt.Sprintf(f, a...))
}

// RunAuto executes the full setup wizard in non-interactive mode.
func RunAuto() {
	state := &SetupState{
		Services:   make(map[string]*ServiceState),
		Keys:       make(map[string]string),
		ManualKeys: make(map[string]string),
		VPNCreds:   make(map[string]string),
		AutoMode:   true,
	}
	runSetup(state)
}

// Run executes the full interactive setup wizard.
func Run() {
	state := &SetupState{
		Services:   make(map[string]*ServiceState),
		Keys:       make(map[string]string),
		ManualKeys: make(map[string]string),
		VPNCreds:   make(map[string]string),
	}
	runSetup(state)
}

func runSetup(state *SetupState) {

	var results []StepResult

	// Phase 0: Service Selection
	ui.PhaseHeader(0, "Service Selection", "Pick services for your stack")
	r := SelectServices(state)
	results = append(results, r)
	ui.PhaseSummary(r.Name, r.Passed, r.Fixed, r.Skipped, len(r.Errors))

	// Phase 1: Environment Detection
	ui.PhaseHeader(1, "Environment Detection", "Data path, timezone, compose dir, Docker detection")
	r = Detect(state)
	results = append(results, r)
	ui.PhaseSummary(r.Name, r.Passed, r.Fixed, r.Skipped, len(r.Errors))

	// Phase 2: Deploy Stack
	ui.PhaseHeader(2, "Deploy Stack", "Deploy missing services via Docker Compose")
	r = DeployStack(state)
	results = append(results, r)
	ui.PhaseSummary(r.Name, r.Passed, r.Fixed, r.Skipped, len(r.Errors))

	// Phase 3: Service Connectivity
	ui.PhaseHeader(3, "Service Connectivity", "HTTP reachability + restart offers")
	r = CheckConnectivity(state)
	results = append(results, r)
	ui.PhaseSummary(r.Name, r.Passed, r.Fixed, r.Skipped, len(r.Errors))

	// Phase 4: API Key Discovery
	ui.PhaseHeader(4, "API Key Discovery", "Auto from containers + manual prompt")
	r = ValidateAPIKeys(state)
	results = append(results, r)
	ui.PhaseSummary(r.Name, r.Passed, r.Fixed, r.Skipped, len(r.Errors))

	// Phase 5: Download Clients
	ui.PhaseHeader(5, "Download Clients", "qBittorrent in Radarr/Sonarr + categories")
	r = ConfigureDownloadClients(state)
	results = append(results, r)
	ui.PhaseSummary(r.Name, r.Passed, r.Fixed, r.Skipped, len(r.Errors))

	// Phase 6: Root Folders
	ui.PhaseHeader(6, "Root Folders", "TRaSH directory structure + *Arr root folders")
	r = ValidateRootFolders(state)
	results = append(results, r)
	ui.PhaseSummary(r.Name, r.Passed, r.Fixed, r.Skipped, len(r.Errors))

	// Phase 7: Prowlarr Wiring
	ui.PhaseHeader(7, "Prowlarr Wiring", "FlareSolverr proxy + indexers + sync targets")
	r = VerifyIndexers(state)
	results = append(results, r)
	ui.PhaseSummary(r.Name, r.Passed, r.Fixed, r.Skipped, len(r.Errors))

	// Phase 8: Seerr Wiring
	ui.PhaseHeader(8, "Seerr Wiring", "Connect to Radarr/Sonarr/media server")
	r = WireSeerr(state)
	results = append(results, r)
	ui.PhaseSummary(r.Name, r.Passed, r.Fixed, r.Skipped, len(r.Errors))

	// Phase 9: Bazarr Wiring
	ui.PhaseHeader(9, "Bazarr Wiring", "Connect to Radarr/Sonarr")
	r = WireBazarr(state)
	results = append(results, r)
	ui.PhaseSummary(r.Name, r.Passed, r.Fixed, r.Skipped, len(r.Errors))

	// Phase 10: Quality Profiles
	ui.PhaseHeader(10, "Quality Profiles", "Sync across library")
	r = SyncQualityProfiles(state)
	results = append(results, r)
	ui.PhaseSummary(r.Name, r.Passed, r.Fixed, r.Skipped, len(r.Errors))

	// Phase 11: Write Config
	ui.PhaseHeader(11, "Write Config", "Save + final summary")
	r = WriteConfig(state)
	results = append(results, r)
	ui.PhaseSummary(r.Name, r.Passed, r.Fixed, r.Skipped, len(r.Errors))

	// Final summary
	printFinalSummary(state, results)
}

func printFinalSummary(state *SetupState, results []StepResult) {
	fmt.Println()
	fmt.Printf("  %s %s\n", ui.GoldText("⚓"), ui.Bold("SETUP COMPLETE"))
	fmt.Println(ui.Separator())

	// Phase breakdown table
	fmt.Println()
	phaseNames := []string{
		"Service Selection",
		"Environment Detection",
		"Deploy Stack",
		"Service Connectivity",
		"API Key Discovery",
		"Download Clients",
		"Root Folders",
		"Prowlarr Wiring",
		"Seerr Wiring",
		"Bazarr Wiring",
		"Quality Profiles",
		"Write Config",
	}

	for i, r := range results {
		name := r.Name
		if i < len(phaseNames) {
			name = phaseNames[i]
		}
		result := formatPhaseResult(r)
		fmt.Printf("  %2d. %-28s %s\n", i, name, result)
	}

	// Totals
	totalPassed, totalFixed, totalSkipped, totalErrors := 0, 0, 0, 0
	for _, r := range results {
		totalPassed += r.Passed
		totalFixed += r.Fixed
		totalSkipped += r.Skipped
		totalErrors += len(r.Errors)
	}

	fmt.Println()
	if totalErrors == 0 {
		fmt.Printf("  Total: %s, %s, %s\n",
			ui.Ok(fmt.Sprintf("%d passed", totalPassed)),
			ui.GoldText(fmt.Sprintf("%d fixed", totalFixed)),
			ui.Dim(fmt.Sprintf("%d skipped", totalSkipped)))
	} else {
		fmt.Printf("  Total: %s, %s, %s, %s\n",
			ui.Ok(fmt.Sprintf("%d passed", totalPassed)),
			ui.GoldText(fmt.Sprintf("%d fixed", totalFixed)),
			ui.Dim(fmt.Sprintf("%d skipped", totalSkipped)),
			ui.Err(fmt.Sprintf("%d error(s)", totalErrors)))
		fmt.Println()
		for _, r := range results {
			for _, e := range r.Errors {
				fmt.Printf("  %s [%s] %s\n", ui.Err("✗"), r.Name, e)
			}
		}
	}

	// Next steps (dynamic)
	fmt.Println()
	fmt.Printf("  %s\n", ui.Bold("Next steps:"))
	fmt.Printf("  %s Run %s to see your fleet dashboard\n", ui.Dim("→"), ui.GoldText("admirarr status"))
	fmt.Printf("  %s Run %s to verify everything is healthy\n", ui.Dim("→"), ui.GoldText("admirarr doctor"))

	// Dynamic next steps based on what happened
	if hasService(state, "jellyfin") && wasDeployed(state, "jellyfin") && state.Keys["jellyfin"] == "" {
		fmt.Printf("  %s Complete Jellyfin setup at %s\n", ui.Dim("→"), ui.CyanText("http://localhost:8096"))
	}
	if hasService(state, "gluetun") && wasDeployed(state, "gluetun") && len(state.VPNCreds) == 0 {
		composeDir := state.ComposeDir
		if composeDir == "" {
			composeDir = "~/docker"
		}
		fmt.Printf("  %s Configure VPN credentials in %s\n", ui.Dim("→"), ui.CyanText(composeDir+"/.env"))
	}
	if hasService(state, "seerr") {
		// Check if media server wiring was skipped
		for _, r := range results {
			if r.Name == "Seerr Wiring" && r.Skipped > 0 {
				fmt.Printf("  %s Complete Seerr media server setup at %s\n", ui.Dim("→"), ui.CyanText("http://localhost:5055/settings"))
				break
			}
		}
	}

	fmt.Println()
}

func formatPhaseResult(r StepResult) string {
	parts := []string{}
	if r.Passed > 0 {
		parts = append(parts, ui.Ok(fmt.Sprintf("%d passed", r.Passed)))
	}
	if r.Fixed > 0 {
		parts = append(parts, ui.GoldText(fmt.Sprintf("%d fixed", r.Fixed)))
	}
	if r.Skipped > 0 {
		parts = append(parts, ui.Dim(fmt.Sprintf("%d skipped", r.Skipped)))
	}
	if len(r.Errors) > 0 {
		parts = append(parts, ui.Err(fmt.Sprintf("%d error(s)", len(r.Errors))))
	}
	return strings.Join(parts, ", ")
}

func hasService(state *SetupState, name string) bool {
	for _, s := range state.SelectedServices {
		if s == name {
			return true
		}
	}
	return false
}

func wasDeployed(state *SetupState, name string) bool {
	svc := state.Services[name]
	return svc != nil && svc.IsDocker && svc.Detected
}
