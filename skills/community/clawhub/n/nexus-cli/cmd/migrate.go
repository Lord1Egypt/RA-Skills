package cmd

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/maxtechera/admirarr/internal/migrate"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var migrateCmd = &cobra.Command{
	Use:   "migrate",
	Short: "Generate Docker Compose stack for the Admirarr setup",
	Long: `Generate a Docker Compose stack following TRaSH Guides best practices.

Creates:
  - docker-compose.yml with selected services
  - .env file with configuration variables
  - TRaSH Guides directory structure (/data/torrents/, /data/media/)
  - Per-service config directories

Detects any running services and harvests API keys before generating.
Use --dry-run to preview without writing files.`,
	Example: `  admirarr migrate
  admirarr migrate --dry-run
  admirarr migrate --compose-dir ~/docker --data-dir /data`,
	Run: runMigrate,
}

var (
	migrateDryRun    bool
	migrateCompose   string
	migrateDataDir   string
	migrateConfigDir string
)

func init() {
	rootCmd.AddCommand(migrateCmd)
	migrateCmd.Flags().BoolVar(&migrateDryRun, "dry-run", false, "Preview changes without writing files")
	migrateCmd.Flags().StringVar(&migrateCompose, "compose-dir", filepath.Join(os.Getenv("HOME"), "docker"), "Directory for docker-compose.yml")
	migrateCmd.Flags().StringVar(&migrateDataDir, "data-dir", "/data", "Data volume root (TRaSH Guides structure)")
	migrateCmd.Flags().StringVar(&migrateConfigDir, "config-dir", "", "Config directory for services (default: <compose-dir>/config)")
}

func runMigrate(cmd *cobra.Command, args []string) {
	ui.PrintBanner()
	fmt.Println(ui.Bold("\n  Admirarr Stack Migration\n"))

	if migrateDryRun {
		fmt.Printf("  %s\n\n", ui.Warn("DRY RUN — no files will be written"))
	}

	result := migrate.Run(migrate.Options{
		ComposeDir: migrateCompose,
		DataDir:    migrateDataDir,
		ConfigDir:  migrateConfigDir,
		DryRun:     migrateDryRun,
	})

	fmt.Println(ui.Bold("\n  Summary"))
	fmt.Println(ui.Separator())

	if result.ComposePath != "" {
		fmt.Printf("  %s Compose: %s\n", ui.Ok("✓"), result.ComposePath)
	}
	if result.EnvPath != "" {
		fmt.Printf("  %s Env:     %s\n", ui.Ok("✓"), result.EnvPath)
	}
	fmt.Printf("  %s Dirs:    %d created\n", ui.Ok("✓"), len(result.DirsCreated))
	fmt.Printf("  %s Keys:    %d harvested\n", ui.Ok("✓"), len(result.KeysFound))

	if len(result.Errors) > 0 {
		fmt.Printf("\n  %s\n", ui.Err(fmt.Sprintf("%d error(s):", len(result.Errors))))
		for _, e := range result.Errors {
			fmt.Printf("    %s %s\n", ui.Err("—"), e)
		}
	}

	if !migrateDryRun && len(result.Errors) == 0 {
		fmt.Printf("\n  %s\n", ui.GoldText("Next steps:"))
		fmt.Printf("    1. Review %s\n", result.ComposePath)
		fmt.Printf("    2. Edit %s with your VPN credentials\n", result.EnvPath)
		fmt.Printf("    3. cd %s && docker compose up -d\n", migrateCompose)
		fmt.Printf("    4. Run 'admirarr setup' to configure services\n")
	}
	fmt.Println()
}
