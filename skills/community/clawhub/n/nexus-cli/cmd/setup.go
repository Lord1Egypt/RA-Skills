package cmd

import (
	"fmt"

	"github.com/maxtechera/admirarr/internal/setup"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var setupCmd = &cobra.Command{
	Use:   "setup",
	Short: "Setup wizard — deploy, configure, and wire your entire stack",
	Long: `Interactive setup wizard that deploys, configures, and wires your entire
Jellyfin + *Arr media server stack in one pass. Each phase will validate and
auto-fix your configuration.

Runs 12 phases:
   0. Service Selection        — pick services for the stack
   1. Environment Detection    — data path, timezone, compose dir, Docker detection
   2. Deploy Stack             — compose generation + docker compose up
   3. Service Connectivity     — HTTP reachability + restart offers
   4. API Key Discovery        — auto from containers + manual prompt
   5. Download Clients         — qBittorrent in Radarr/Sonarr + categories
   6. Root Folders             — TRaSH directory structure + *Arr root folders
   7. Prowlarr Wiring          — FlareSolverr proxy + indexers + sync targets
   8. Seerr Wiring             — connect to Radarr/Sonarr/media server
   9. Bazarr Wiring            — connect to Radarr/Sonarr
  10. Quality Profiles          — sync across library
  11. Write Config              — save + final summary`,
	Example: "  admirarr setup\n  admirarr setup --auto",
	Run:     runSetup,
}

var setupAutoFlag bool

func init() {
	setupCmd.Flags().BoolVar(&setupAutoFlag, "auto", false, "Non-interactive mode — use detected defaults, skip all prompts")
	rootCmd.AddCommand(setupCmd)
}

func runSetup(cmd *cobra.Command, args []string) {
	ui.PrintBanner()
	fmt.Println()
	if setupAutoFlag {
		fmt.Printf("  %s %s\n", ui.GoldText("⚓"), ui.Bold("Setup Wizard — auto mode"))
	} else {
		fmt.Printf("  %s %s\n", ui.GoldText("⚓"), ui.Bold("Setup Wizard — deploy and configure your fleet"))
	}
	fmt.Println(ui.Separator())

	if setupAutoFlag {
		setup.RunAuto()
	} else {
		setup.Run()
	}
}
