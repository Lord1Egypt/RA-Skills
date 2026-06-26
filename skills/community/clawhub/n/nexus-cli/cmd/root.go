package cmd

import (
	"fmt"
	"os"

	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "admirarr",
	Short: "Command your fleet — manage your Jellyfin + *Arr media server stack",
	Long: fmt.Sprintf(`%s %s %s    %s

Admirarr is a CLI for managing your Jellyfin + *Arr media server stack.
It provides dashboard views, diagnostics, search, and management commands
for Jellyfin, Radarr, Sonarr, Prowlarr, qBittorrent, and more.`,
		ui.GoldText("⚓"), ui.Bold("ADMIRARR"), ui.Dim("v"+ui.Version), ui.Dim("Command your fleet.")),
	Version: ui.Version,
	Run: func(cmd *cobra.Command, args []string) {
		ui.PrintLogo()
		_ = cmd.Help()
	},
}

// Execute runs the root command.
func Execute() {
	config.Load()
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func init() {
	rootCmd.PersistentFlags().StringVarP(&ui.OutputFormat, "output", "o", "text", "Output format: text or json")
	rootCmd.SetVersionTemplate(fmt.Sprintf("admirarr v%s\n", ui.Version))
	rootCmd.CompletionOptions.HiddenDefaultCmd = true
}
