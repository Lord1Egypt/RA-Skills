package cmd

import (
	"fmt"
	"os/exec"
	"strings"

	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var dockerCmd = &cobra.Command{
	Use:   "docker",
	Short: "Docker container status",
	Long: `Show Docker container status for all media stack containers.

Uses docker compose ps (or docker ps) to show all containers
in the compose project.`,
	Example: "  admirarr docker",
	Run:     runDocker,
}

func init() {
	rootCmd.AddCommand(dockerCmd)
}

func runDocker(cmd *cobra.Command, args []string) {
	// Try docker compose ps first (shows all project containers)
	out, err := exec.Command("docker", "compose", "ps", "-a", "--format", "{{.Name}}\t{{.Status}}").Output()
	if err != nil || strings.TrimSpace(string(out)) == "" {
		// Fall back to docker ps filtered by registered container names
		dockerArgs := []string{"ps", "-a", "--format", "{{.Names}}\t{{.Status}}\t{{.Ports}}"}
		for _, name := range config.AllRegisteredNames() {
			if cn := config.ContainerName(name); cn != "" {
				dockerArgs = append(dockerArgs, "--filter", "name="+cn)
			}
		}
		out, err = exec.Command("docker", dockerArgs...).Output()
		if err != nil {
			if ui.IsJSON() {
				ui.PrintJSON([]struct{}{})
			} else {
				ui.PrintBanner()
				fmt.Println(ui.Bold("\n  Docker Containers\n"))
				fmt.Printf("  %s\n", ui.Dim("No containers found"))
				fmt.Println()
			}
			return
		}
	}

	lines := strings.TrimSpace(string(out))
	if lines == "" {
		if ui.IsJSON() {
			ui.PrintJSON([]struct{}{})
		} else {
			ui.PrintBanner()
			fmt.Println(ui.Bold("\n  Docker Containers\n"))
			fmt.Printf("  %s\n", ui.Dim("No containers found"))
			fmt.Println()
		}
		return
	}

	type containerOut struct {
		Name   string `json:"name"`
		Status string `json:"status"`
	}
	var jsonOut []containerOut

	for _, line := range strings.Split(lines, "\n") {
		parts := strings.SplitN(line, "\t", 3)
		name := "?"
		status := "?"
		if len(parts) > 0 {
			name = parts[0]
		}
		if len(parts) > 1 {
			status = parts[1]
		}
		jsonOut = append(jsonOut, containerOut{Name: name, Status: status})
	}

	ui.PrintOrJSON(jsonOut, func() {
		ui.PrintBanner()
		fmt.Println(ui.Bold("\n  Docker Containers\n"))
		for _, c := range jsonOut {
			colorFn := ui.Err
			if strings.Contains(c.Status, "Up") || strings.Contains(c.Status, "running") {
				colorFn = ui.Ok
			}
			fmt.Printf("  %-20s %s\n", c.Name, colorFn(c.Status))
		}
		fmt.Println()
	})
}
