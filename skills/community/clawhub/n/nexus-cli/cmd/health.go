package cmd

import (
	"fmt"

	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var healthCmd = &cobra.Command{
	Use:   "health",
	Short: "Health warnings from Jellyfin, Radarr, Sonarr, and Prowlarr",
	Long: `Show health warnings from Jellyfin and *Arr services.

Queries the health endpoint of each service and displays warnings.

API endpoints used:
  Jellyfin   GET /System/Info/Public
  Radarr     GET /api/v3/health
  Sonarr     GET /api/v3/health
  Prowlarr   GET /api/v1/health`,
	Example: "  admirarr health",
	Run:     runHealth,
}

func init() {
	rootCmd.AddCommand(healthCmd)
}

func runHealth(cmd *cobra.Command, args []string) {
	type healthOut struct {
		Service string `json:"service"`
		Type    string `json:"type"`
		Message string `json:"message"`
	}

	var results []healthOut

	// Jellyfin health check
	if api.CheckReachable("jellyfin") {
		results = append(results, healthOut{Service: "jellyfin", Type: "ok", Message: "Healthy"})
	} else {
		results = append(results, healthOut{Service: "jellyfin", Type: "error", Message: "unreachable"})
	}

	// *Arr health checks
	for _, svc := range []string{"radarr", "sonarr", "prowlarr"} {
		items, err := arr.New(svc).Health()
		if err != nil || len(items) == 0 {
			results = append(results, healthOut{Service: svc, Type: "ok", Message: "Healthy"})
			continue
		}
		for _, item := range items {
			results = append(results, healthOut{Service: svc, Type: item.Type, Message: item.Message})
		}
	}

	ui.PrintOrJSON(results, func() {
		ui.PrintBanner()
		fmt.Println(ui.Bold("\n  Health Check\n"))
		for _, r := range results {
			if r.Type == "ok" {
				fmt.Printf("  %s %s Healthy\n", ui.Ok("●"), ui.Dim("["+r.Service+"]"))
			} else {
				level := ui.Warn("WARN")
				if r.Type == "error" {
					level = ui.Err("ERROR")
				}
				fmt.Printf("  %s %s %s\n", level, ui.Dim("["+r.Service+"]"), r.Message)
			}
		}
		fmt.Println()
	})
}
