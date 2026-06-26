package cmd

import (
	"fmt"
	"os/exec"
	"strings"

	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var restartCmd = &cobra.Command{
	Use:   "restart <service>",
	Short: "Restart a service",
	Long: `Restart a service managed by Admirarr.

Supports multiple deployment types:
  - Docker: runs docker restart on the container
  - Native/Remote *Arr services: uses the /api/{ver}/system/restart endpoint
  - Services without a restart API: reports that a manual restart is needed`,
	Example: "  admirarr restart sonarr\n  admirarr restart radarr\n  admirarr restart seerr",
	Args:    cobra.ExactArgs(1),
	Run:     runRestart,
}

func init() {
	rootCmd.AddCommand(restartCmd)
}

func runRestart(cmd *cobra.Command, args []string) {
	service := strings.ToLower(args[0])

	rt := config.DetectRuntime(service)

	switch rt.Type {
	case config.TypeDocker:
		restartDocker(service)
	case config.TypeNative, config.TypeRemote:
		restartViaAPI(service)
	}
}

// restartDocker restarts a service via docker restart.
func restartDocker(service string) {
	container := config.ContainerName(service)

	if !ui.IsJSON() {
		fmt.Printf("  Restarting %s (container: %s)...\n", service, container)
	}

	out, err := exec.Command("docker", "restart", container).CombinedOutput()
	if err != nil {
		printResult(service, "error", strings.TrimSpace(string(out)))
	} else {
		printResult(service, "ok", fmt.Sprintf("Restarted %s", service))
	}
}

// restartViaAPI restarts a native/remote service. *Arr services expose a
// restart endpoint; others require a manual restart.
func restartViaAPI(service string) {
	apiVer := config.ServiceAPIVer(service)

	// *Arr services (radarr, sonarr, prowlarr, lidarr, readarr, whisparr)
	// expose POST /api/{ver}/system/restart.
	if apiVer != "" {
		if !ui.IsJSON() {
			fmt.Printf("  Restarting %s via API...\n", service)
		}

		endpoint := fmt.Sprintf("api/%s/system/restart", apiVer)
		_, err := api.Post(service, endpoint, nil, nil)
		if err != nil {
			printResult(service, "error", fmt.Sprintf("API restart failed: %v", err))
		} else {
			printResult(service, "ok", fmt.Sprintf("Restarted %s via API", service))
		}
		return
	}

	// Services without a restart API (qBittorrent, Plex, etc.).
	msg := fmt.Sprintf("%s does not support API restart — please restart it manually", service)
	printResult(service, "manual", msg)
}

// printResult outputs the restart result in either JSON or human-readable form.
func printResult(service, status, message string) {
	if ui.IsJSON() {
		ui.PrintJSON(map[string]string{
			"service": service,
			"status":  status,
			"message": message,
		})
		return
	}

	switch status {
	case "ok":
		fmt.Printf("  %s %s\n", ui.Ok("●"), message)
	case "manual":
		fmt.Printf("  %s %s\n", ui.Warn("●"), message)
	default:
		fmt.Printf("  %s %s\n", ui.Err("Failed:"), message)
	}
	fmt.Println()
}
