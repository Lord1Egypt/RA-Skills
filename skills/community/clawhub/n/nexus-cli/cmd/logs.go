package cmd

import (
	"fmt"
	"os/exec"
	"strings"
	"time"

	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/keys"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var logsCmd = &cobra.Command{
	Use:   "logs <service>",
	Short: "Recent logs from a service",
	Long: `View recent logs from a service.

For *Arr services (sonarr, radarr, prowlarr), fetches structured logs via API.
For other services, uses docker logs as fallback.`,
	Example: "  admirarr logs sonarr\n  admirarr logs radarr\n  admirarr logs jellyfin",
	Args:    cobra.ExactArgs(1),
	Run:     runLogs,
}

func init() {
	rootCmd.AddCommand(logsCmd)
}

func runLogs(cmd *cobra.Command, args []string) {
	service := strings.ToLower(args[0])

	type logOut struct {
		Time    string `json:"time"`
		Level   string `json:"level"`
		Message string `json:"message"`
	}

	// For *Arr services, use the structured log API
	ver := config.ServiceAPIVer(service)
	if ver != "" {
		var data struct {
			Records []struct {
				Level   string `json:"level"`
				Message string `json:"message"`
				Time    string `json:"time"`
			} `json:"records"`
		}
		params := map[string]string{
			"pageSize":      "20",
			"sortDirection": "descending",
			"sortKey":       "time",
		}
		if err := api.GetJSON(service, fmt.Sprintf("api/%s/log", ver), params, &data); err == nil {
			var out []logOut
			for _, rec := range data.Records {
				out = append(out, logOut{Time: rec.Time, Level: rec.Level, Message: rec.Message})
			}
			ui.PrintOrJSON(out, func() {
				printLogRecords(service, data.Records)
			})
			return
		}
	}

	// Service-specific log endpoints for non-*Arr services
	switch service {
	case "jellyfin":
		if fetchJellyfinLogs(service) {
			return
		}
	case "plex":
		printPlexLogHint(service)
		return
	case "qbittorrent":
		if fetchQBittorrentLogs(service) {
			return
		}
	case "tautulli":
		if fetchTautulliLogs(service) {
			return
		}
	}

	// Fallback: docker logs (only for Docker-managed services)
	rt := config.DetectRuntime(service)
	if rt.Type != config.TypeDocker {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": fmt.Sprintf("No log source available for %s (%s)", service, rt.Label)})
		} else {
			ui.PrintBanner()
			fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  %s — Recent Logs\n", capitalize(service))))
			fmt.Printf("  %s\n", ui.Err(fmt.Sprintf("No log source available for %s (non-Docker service)", service)))
		}
		return
	}

	container := config.ContainerName(service)
	out, err := exec.Command("docker", "logs", "--tail", "30", container).CombinedOutput()
	if err != nil {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": fmt.Sprintf("Cannot get logs for %s", service)})
		} else {
			ui.PrintBanner()
			fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  %s — Recent Logs\n", capitalize(service))))
			fmt.Printf("  %s\n", ui.Err(fmt.Sprintf("Cannot get logs for %s", service)))
		}
		return
	}

	lines := strings.TrimSpace(string(out))
	if lines == "" {
		if ui.IsJSON() {
			ui.PrintJSON([]logOut{})
		} else {
			ui.PrintBanner()
			fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  %s — Recent Logs\n", capitalize(service))))
			fmt.Printf("  %s\n", ui.Dim("No logs"))
		}
		return
	}

	var logResults []logOut
	for _, line := range strings.Split(lines, "\n") {
		logResults = append(logResults, logOut{Time: "", Level: "info", Message: line})
	}

	ui.PrintOrJSON(logResults, func() {
		ui.PrintBanner()
		fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  %s — Recent Logs\n", capitalize(service))))
		for _, line := range strings.Split(lines, "\n") {
			fmt.Printf("  %s\n", line)
		}
		fmt.Println()
	})
}

// printLogRecords renders structured *Arr-style log records to the terminal.
func printLogRecords(service string, records []struct {
	Level   string `json:"level"`
	Message string `json:"message"`
	Time    string `json:"time"`
}) {
	ui.PrintBanner()
	fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  %s — Recent Logs\n", capitalize(service))))
	for _, rec := range records {
		msg := rec.Message
		if len(msg) > 100 {
			msg = msg[:100]
		}
		t := rec.Time
		if len(t) > 19 {
			t = t[:19]
		}
		colorFn := ui.Dim
		if rec.Level == "error" {
			colorFn = ui.Err
		} else if rec.Level == "warn" {
			colorFn = ui.Warn
		}
		fmt.Printf("  %s %8s  %s\n", ui.Dim(t), colorFn(rec.Level), msg)
	}
	fmt.Println()
}

// printGenericLines renders plain log lines to the terminal.
func printGenericLines(service string, lines []string) {
	type logOut struct {
		Time    string `json:"time"`
		Level   string `json:"level"`
		Message string `json:"message"`
	}
	var results []logOut
	for _, line := range lines {
		results = append(results, logOut{Time: "", Level: "info", Message: line})
	}
	ui.PrintOrJSON(results, func() {
		ui.PrintBanner()
		fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  %s — Recent Logs\n", capitalize(service))))
		for _, line := range lines {
			fmt.Printf("  %s\n", line)
		}
		fmt.Println()
	})
}

// fetchJellyfinLogs retrieves logs from the Jellyfin System/Log API.
func fetchJellyfinLogs(service string) bool {
	logName := fmt.Sprintf("log_%s.log", time.Now().Format("20060102"))
	var body string
	if err := api.GetJSON(service, fmt.Sprintf("System/Log/Name/%s", logName), nil, &body); err != nil {
		return false
	}
	raw := strings.TrimSpace(body)
	if raw == "" {
		return false
	}
	all := strings.Split(raw, "\n")
	// Show last 30 lines
	start := 0
	if len(all) > 30 {
		start = len(all) - 30
	}
	printGenericLines(service, all[start:])
	return true
}

// printPlexLogHint shows the user where to find Plex logs (no standard API).
func printPlexLogHint(service string) {
	type logOut struct {
		Time    string `json:"time"`
		Level   string `json:"level"`
		Message string `json:"message"`
	}
	msg := "Plex has no standard log API. Check logs at: " +
		"Linux: /var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs/ | " +
		"Windows: %%LOCALAPPDATA%%\\Plex Media Server\\Logs\\ | " +
		"macOS: ~/Library/Application Support/Plex Media Server/Logs/"
	if ui.IsJSON() {
		ui.PrintJSON([]logOut{{Message: msg, Level: "info"}})
	} else {
		ui.PrintBanner()
		fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  %s — Recent Logs\n", capitalize(service))))
		fmt.Printf("  %s\n\n", ui.Dim("Plex has no standard log API. Check logs directly:"))
		fmt.Printf("  %s  %s\n", ui.Bold("Linux:"), "/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs/")
		fmt.Printf("  %s  %s\n", ui.Bold("Windows:"), `%LOCALAPPDATA%\Plex Media Server\Logs\`)
		fmt.Printf("  %s  %s\n", ui.Bold("macOS:"), "~/Library/Application Support/Plex Media Server/Logs/")
		fmt.Println()
	}
}

// fetchQBittorrentLogs retrieves logs from the qBittorrent web API.
func fetchQBittorrentLogs(service string) bool {
	var entries []struct {
		ID        int    `json:"id"`
		Message   string `json:"message"`
		Timestamp int64  `json:"timestamp"`
		Type      int    `json:"type"`
	}
	params := map[string]string{
		"last_known_id": "-1",
		"normal":        "true",
		"info":          "true",
		"warning":       "true",
		"critical":      "true",
	}
	if err := api.GetJSON(service, "api/v2/log/main", params, &entries); err != nil {
		return false
	}
	if len(entries) == 0 {
		return false
	}
	// Show last 30 entries
	start := 0
	if len(entries) > 30 {
		start = len(entries) - 30
	}
	type logOut struct {
		Time    string `json:"time"`
		Level   string `json:"level"`
		Message string `json:"message"`
	}
	var results []logOut
	for _, e := range entries[start:] {
		level := "info"
		switch e.Type {
		case 2:
			level = "warn"
		case 4:
			level = "error"
		}
		t := time.Unix(e.Timestamp/1000, 0).Format("2006-01-02T15:04:05")
		results = append(results, logOut{Time: t, Level: level, Message: e.Message})
	}
	ui.PrintOrJSON(results, func() {
		ui.PrintBanner()
		fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  %s — Recent Logs\n", capitalize(service))))
		for _, rec := range results {
			msg := rec.Message
			if len(msg) > 100 {
				msg = msg[:100]
			}
			colorFn := ui.Dim
			if rec.Level == "error" {
				colorFn = ui.Err
			} else if rec.Level == "warn" {
				colorFn = ui.Warn
			}
			fmt.Printf("  %s %8s  %s\n", ui.Dim(rec.Time), colorFn(rec.Level), msg)
		}
		fmt.Println()
	})
	return true
}

// fetchTautulliLogs retrieves logs from the Tautulli API.
func fetchTautulliLogs(service string) bool {
	apiKey := keys.Get(service)
	if apiKey == "" {
		return false
	}
	var data struct {
		Response struct {
			Data []struct {
				Timestamp int64  `json:"timestamp"`
				Message   string `json:"msg"`
				Level     string `json:"loglevel"`
			} `json:"data"`
		} `json:"response"`
	}
	params := map[string]string{
		"apikey": apiKey,
		"cmd":    "get_logs",
	}
	if err := api.GetJSON(service, "api/v2", params, &data); err != nil {
		return false
	}
	if len(data.Response.Data) == 0 {
		return false
	}
	type logOut struct {
		Time    string `json:"time"`
		Level   string `json:"level"`
		Message string `json:"message"`
	}
	var results []logOut
	for _, e := range data.Response.Data {
		t := ""
		if e.Timestamp > 0 {
			t = time.Unix(e.Timestamp, 0).Format("2006-01-02T15:04:05")
		}
		level := strings.ToLower(e.Level)
		if level == "" {
			level = "info"
		}
		results = append(results, logOut{Time: t, Level: level, Message: e.Message})
	}
	// Show last 30
	start := 0
	if len(results) > 30 {
		start = len(results) - 30
	}
	results = results[start:]
	ui.PrintOrJSON(results, func() {
		ui.PrintBanner()
		fmt.Printf("%s\n", ui.Bold(fmt.Sprintf("\n  %s — Recent Logs\n", capitalize(service))))
		for _, rec := range results {
			msg := rec.Message
			if len(msg) > 100 {
				msg = msg[:100]
			}
			colorFn := ui.Dim
			if rec.Level == "error" {
				colorFn = ui.Err
			} else if rec.Level == "warn" || rec.Level == "warning" {
				colorFn = ui.Warn
			}
			t := rec.Time
			if len(t) > 19 {
				t = t[:19]
			}
			fmt.Printf("  %s %8s  %s\n", ui.Dim(t), colorFn(rec.Level), msg)
		}
		fmt.Println()
	})
	return true
}

func capitalize(s string) string {
	if len(s) == 0 {
		return s
	}
	return string(s[0]-32) + s[1:]
}
