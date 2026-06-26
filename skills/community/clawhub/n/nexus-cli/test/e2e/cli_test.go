// Package e2e runs end-to-end tests against the admirarr binary.
//
// These tests build the binary once in TestMain, then exercise every command
// by shelling out and inspecting stdout, stderr, and exit codes.
//
// Commands that require live services are tested in two modes:
//   - With --output json to verify structured output and graceful degradation
//   - With text output to verify banner/formatting renders
//
// Run:
//
//	go test ./test/e2e/ -v
//	go test ./test/e2e/ -v -run TestCLI_Status
package e2e

import (
	"encoding/json"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
)

var binary string // path to built admirarr binary

func TestMain(m *testing.M) {
	// Build the binary once for all tests
	dir, err := os.MkdirTemp("", "admirarr-e2e-*")
	if err != nil {
		panic("cannot create temp dir: " + err.Error())
	}
	binary = filepath.Join(dir, "admirarr")

	cmd := exec.Command("go", "build",
		"-ldflags", "-X github.com/maxtechera/admirarr/internal/ui.Version=test",
		"-o", binary, ".")
	cmd.Dir = filepath.Join("..", "..")
	if out, err := cmd.CombinedOutput(); err != nil {
		panic("build failed: " + string(out))
	}

	code := m.Run()
	os.RemoveAll(dir)
	os.Exit(code)
}

// run executes the binary with args and returns stdout, stderr, exit code.
func run(args ...string) (stdout, stderr string, exitCode int) {
	cmd := exec.Command(binary, args...)
	var outBuf, errBuf strings.Builder
	cmd.Stdout = &outBuf
	cmd.Stderr = &errBuf
	err := cmd.Run()
	exitCode = 0
	if err != nil {
		if exitErr, ok := err.(*exec.ExitError); ok {
			exitCode = exitErr.ExitCode()
		} else {
			exitCode = -1
		}
	}
	return outBuf.String(), errBuf.String(), exitCode
}

// runJSON executes a command with --output json and unmarshals stdout.
func runJSON(t *testing.T, target interface{}, args ...string) {
	t.Helper()
	args = append(args, "--output", "json")
	stdout, _, code := run(args...)
	if code != 0 {
		t.Fatalf("command %v exited %d: %s", args, code, stdout)
	}
	if err := json.Unmarshal([]byte(stdout), target); err != nil {
		t.Fatalf("invalid JSON from %v: %v\nraw: %s", args, err, stdout)
	}
}

// ════════════════════════════════════════════════════════════════════
// Root command
// ════════════════════════════════════════════════════════════════════

func TestCLI_Help(t *testing.T) {
	stdout, _, code := run("--help")
	if code != 0 {
		t.Fatalf("--help exited %d", code)
	}
	for _, want := range []string{
		"ADMIRARR",
		"Available Commands:",
		"status",
		"doctor",
		"setup",
		"movies",
		"shows",
		"indexers",
		"--output",
	} {
		if !strings.Contains(stdout, want) {
			t.Errorf("--help missing %q", want)
		}
	}
}

func TestCLI_Version(t *testing.T) {
	stdout, _, code := run("--version")
	if code != 0 {
		t.Fatalf("--version exited %d", code)
	}
	if !strings.Contains(stdout, "admirarr") {
		t.Errorf("--version should contain 'admirarr', got: %s", stdout)
	}
}

func TestCLI_UnknownCommand(t *testing.T) {
	_, stderr, code := run("not-a-command")
	if code == 0 {
		t.Fatal("unknown command should exit non-zero")
	}
	if !strings.Contains(stderr, "unknown command") {
		t.Errorf("expected 'unknown command' in stderr, got: %s", stderr)
	}
}

func TestCLI_NoArgs_ShowsHelp(t *testing.T) {
	stdout, _, code := run()
	if code != 0 {
		t.Fatalf("no-args exited %d", code)
	}
	if !strings.Contains(stdout, "Available Commands:") {
		t.Error("no-args should show help with Available Commands")
	}
}

// ════════════════════════════════════════════════════════════════════
// Subcommand help text
// ════════════════════════════════════════════════════════════════════

func TestCLI_SubcommandHelp(t *testing.T) {
	commands := []struct {
		name     string
		wantHelp []string // strings that must appear in --help output
	}{
		{"status", []string{"dashboard", "--live", "--interval"}},
		{"doctor", []string{"diagnostics", "--fix"}},
		{"setup", []string{"wizard", "validate"}},
		{"movies", []string{"Radarr"}},
		{"shows", []string{"Sonarr"}},
		{"indexers", []string{"Prowlarr", "setup", "add", "remove", "test", "sync"}},
		{"downloads", []string{"qBittorrent"}},
		{"queue", []string{"queue"}},
		{"missing", []string{"monitored"}},
		{"requests", []string{"Seerr"}},
		{"search", []string{"Prowlarr", "indexers"}},
		{"health", []string{"health", "warnings"}},
		{"disk", []string{"disk", "space"}},
		{"logs", []string{"logs"}},
		{"recent", []string{"recently", "added"}},
		{"history", []string{"history"}},
		{"scan", []string{"scan"}},
		{"restart", []string{"Restart"}},
		{"docker", []string{"Docker"}},
		{"completion", []string{"completion", "bash"}},
		{"find", []string{"Radarr", "releases"}},
		{"add-movie", []string{"movie", "Radarr"}},
		{"add-show", []string{"show", "Sonarr"}},
	}

	for _, tc := range commands {
		t.Run(tc.name, func(t *testing.T) {
			stdout, _, code := run(tc.name, "--help")
			if code != 0 {
				t.Fatalf("%s --help exited %d", tc.name, code)
			}
			for _, want := range tc.wantHelp {
				if !strings.Contains(stdout, want) {
					t.Errorf("%s --help missing %q", tc.name, want)
				}
			}
		})
	}
}

// ════════════════════════════════════════════════════════════════════
// status
// ════════════════════════════════════════════════════════════════════

func TestCLI_Status_Text(t *testing.T) {
	stdout, _, code := run("status")
	if code != 0 {
		t.Fatalf("status exited %d", code)
	}
	for _, want := range []string{"ADMIRARR", "Fleet", "Library", "Indexers"} {
		if !strings.Contains(stdout, want) {
			t.Errorf("status missing section %q", want)
		}
	}
}

func TestCLI_Status_JSON(t *testing.T) {
	var out struct {
		Services []struct {
			Name      string `json:"name"`
			Host      string `json:"host"`
			Up        bool   `json:"up"`
			LatencyMs int64  `json:"latency_ms"`
		} `json:"services"`
		Library struct {
			Movies       int   `json:"movies"`
			MoviesOnDisk int   `json:"movies_on_disk"`
			Shows        int   `json:"shows"`
			TotalSize    int64 `json:"total_size"`
		} `json:"library"`
		Health   []interface{} `json:"health"`
		Requests []interface{} `json:"requests"`
		Queues   struct {
			Radarr []interface{} `json:"radarr"`
			Sonarr []interface{} `json:"sonarr"`
		} `json:"queues"`
		Torrents []interface{} `json:"torrents"`
	}
	runJSON(t, &out, "status")

	if len(out.Services) == 0 {
		t.Fatal("status JSON should list services")
	}

	// Verify expected services appear
	serviceNames := make(map[string]bool)
	for _, s := range out.Services {
		serviceNames[s.Name] = true
		if s.Name == "" {
			t.Error("service has empty name")
		}
	}
	for _, required := range []string{"radarr", "sonarr", "prowlarr"} {
		if !serviceNames[required] {
			t.Errorf("status JSON missing service %q", required)
		}
	}

	// Arrays should never be null (empty arrays instead)
	if out.Health == nil {
		t.Error("health should be [] not null")
	}
	if out.Requests == nil {
		t.Error("requests should be [] not null")
	}
	if out.Queues.Radarr == nil {
		t.Error("queues.radarr should be [] not null")
	}
	if out.Queues.Sonarr == nil {
		t.Error("queues.sonarr should be [] not null")
	}
	if out.Torrents == nil {
		t.Error("torrents should be [] not null")
	}
}

func TestCLI_Status_JSON_ServiceLatency(t *testing.T) {
	var out struct {
		Services []struct {
			Name      string `json:"name"`
			Up        bool   `json:"up"`
			LatencyMs int64  `json:"latency_ms"`
		} `json:"services"`
	}
	runJSON(t, &out, "status")

	for _, s := range out.Services {
		// Up services must have non-negative latency
		if s.Up && s.LatencyMs < 0 {
			t.Errorf("service %s is up but has negative latency: %d", s.Name, s.LatencyMs)
		}
	}
}

// TestCLI_Status_JSON_RuntimeDetection verifies that services include auto-detected
// runtime info in JSON output and that host comes directly from config.
func TestCLI_Status_JSON_RuntimeDetection(t *testing.T) {
	var out struct {
		Services []struct {
			Name    string `json:"name"`
			Host    string `json:"host"`
			Runtime string `json:"runtime"`
		} `json:"services"`
	}
	runJSON(t, &out, "status")

	for _, s := range out.Services {
		if s.Host == "" {
			t.Errorf("service %s has empty host", s.Name)
		}
		// Every service with a port should have a runtime label
		if s.Runtime == "" {
			t.Errorf("service %s has no runtime label", s.Name)
		}
		// Runtime must be one of the valid types
		switch {
		case s.Runtime == "native",
			s.Runtime == "remote",
			len(s.Runtime) > 7 && s.Runtime[:7] == "docker ":
			// valid
		default:
			t.Errorf("service %s has unexpected runtime %q", s.Name, s.Runtime)
		}
	}
}

// ════════════════════════════════════════════════════════════════════
// doctor
// ════════════════════════════════════════════════════════════════════

func TestCLI_Doctor_Text(t *testing.T) {
	stdout, _, code := run("doctor")
	if code != 0 {
		t.Fatalf("doctor exited %d", code)
	}
	if !strings.Contains(stdout, "ADMIRARR") {
		t.Error("doctor should show banner")
	}
	// Doctor always prints a summary line
	if !strings.Contains(stdout, "checks passed") && !strings.Contains(stdout, "issue") {
		t.Error("doctor should print summary with checks/issues")
	}
}

func TestCLI_Doctor_JSON(t *testing.T) {
	stdout, _, code := run("doctor", "--output", "json")
	if code != 0 {
		t.Fatalf("doctor exited %d", code)
	}

	// Doctor prints progress text followed by a JSON summary on the last line.
	// Extract the last non-empty line which should be JSON.
	lines := strings.Split(strings.TrimSpace(stdout), "\n")
	var jsonLine string
	for i := len(lines) - 1; i >= 0; i-- {
		trimmed := strings.TrimSpace(lines[i])
		if trimmed != "" && (strings.HasPrefix(trimmed, "{") || strings.HasPrefix(trimmed, "[")) {
			jsonLine = trimmed
			break
		}
	}

	if jsonLine == "" {
		t.Fatal("doctor --output json should contain a JSON summary line")
	}

	var out struct {
		ChecksPassed int      `json:"checks_passed"`
		Issues       []string `json:"issues"`
	}
	if err := json.Unmarshal([]byte(jsonLine), &out); err != nil {
		t.Fatalf("doctor JSON summary invalid: %v\nline: %s", err, jsonLine)
	}
	if out.ChecksPassed < 0 {
		t.Error("checks_passed should be non-negative")
	}
}

// ════════════════════════════════════════════════════════════════════
// movies / shows — graceful degradation when services are down
// ════════════════════════════════════════════════════════════════════

func TestCLI_Movies_JSON_ServiceDown(t *testing.T) {
	stdout, _, code := run("movies", "--output", "json")
	if code != 0 {
		t.Fatalf("movies exited %d", code)
	}

	// Should return either an error object or an empty array
	var errObj map[string]string
	var arr []interface{}
	if json.Unmarshal([]byte(stdout), &errObj) == nil {
		if errObj["error"] == "" {
			t.Error("error object should have non-empty error field")
		}
	} else if json.Unmarshal([]byte(stdout), &arr) == nil {
		// Valid: empty array or populated array
	} else {
		t.Errorf("movies JSON should be an error object or array, got: %s", stdout)
	}
}

func TestCLI_Shows_JSON_ServiceDown(t *testing.T) {
	stdout, _, code := run("shows", "--output", "json")
	if code != 0 {
		t.Fatalf("shows exited %d", code)
	}
	var errObj map[string]string
	var arr []interface{}
	if json.Unmarshal([]byte(stdout), &errObj) == nil {
		if errObj["error"] == "" {
			t.Error("error object should have non-empty error field")
		}
	} else if json.Unmarshal([]byte(stdout), &arr) == nil {
		// Valid
	} else {
		t.Errorf("shows JSON should be an error object or array, got: %s", stdout)
	}
}

// ════════════════════════════════════════════════════════════════════
// indexers
// ════════════════════════════════════════════════════════════════════

func TestCLI_Indexers_JSON_ServiceDown(t *testing.T) {
	stdout, _, code := run("indexers", "--output", "json")
	if code != 0 {
		t.Fatalf("indexers exited %d", code)
	}
	var errObj map[string]string
	var arr []interface{}
	if json.Unmarshal([]byte(stdout), &errObj) == nil {
		// Prowlarr down → error object
		if errObj["error"] == "" {
			t.Error("error object should have non-empty error field")
		}
	} else if json.Unmarshal([]byte(stdout), &arr) == nil {
		// Prowlarr up → array of indexers
	} else {
		t.Errorf("indexers JSON should be error or array, got: %s", stdout)
	}
}

func TestCLI_Indexers_Add_NoArg(t *testing.T) {
	_, stderr, code := run("indexers", "add")
	if code == 0 {
		t.Fatal("indexers add with no arg should fail")
	}
	if !strings.Contains(stderr, "requires") || !strings.Contains(stderr, "arg") {
		// cobra says "accepts 1 arg(s), received 0"
		if !strings.Contains(stderr, "arg") {
			t.Errorf("expected arg error, got: %s", stderr)
		}
	}
}

func TestCLI_Indexers_Remove_NoArg(t *testing.T) {
	_, stderr, code := run("indexers", "remove")
	if code == 0 {
		t.Fatal("indexers remove with no arg should fail")
	}
	if !strings.Contains(stderr, "arg") {
		t.Errorf("expected arg error, got: %s", stderr)
	}
}

// ════════════════════════════════════════════════════════════════════
// health
// ════════════════════════════════════════════════════════════════════

func TestCLI_Health_JSON(t *testing.T) {
	stdout, _, code := run("health", "--output", "json")
	if code != 0 {
		t.Fatalf("health exited %d", code)
	}
	// Should be a JSON array (possibly empty)
	var arr []interface{}
	if err := json.Unmarshal([]byte(stdout), &arr); err != nil {
		t.Fatalf("health JSON should be array: %v\nraw: %s", err, stdout)
	}
}

// ════════════════════════════════════════════════════════════════════
// disk
// ════════════════════════════════════════════════════════════════════

func TestCLI_Disk_Text(t *testing.T) {
	stdout, _, code := run("disk")
	if code != 0 {
		t.Fatalf("disk exited %d", code)
	}
	if !strings.Contains(stdout, "Disk") {
		t.Error("disk output should contain 'Disk'")
	}
}

func TestCLI_Disk_JSON(t *testing.T) {
	stdout, _, code := run("disk", "--output", "json")
	if code != 0 {
		t.Fatalf("disk exited %d", code)
	}
	var out interface{}
	if err := json.Unmarshal([]byte(stdout), &out); err != nil {
		t.Fatalf("disk JSON invalid: %v\nraw: %s", err, stdout)
	}
}

// ════════════════════════════════════════════════════════════════════
// docker
// ════════════════════════════════════════════════════════════════════

func TestCLI_Docker_JSON(t *testing.T) {
	stdout, _, code := run("docker", "--output", "json")
	if code != 0 {
		t.Fatalf("docker exited %d", code)
	}
	var arr []interface{}
	if err := json.Unmarshal([]byte(stdout), &arr); err != nil {
		t.Fatalf("docker JSON should be array: %v\nraw: %s", err, stdout)
	}
}

// ════════════════════════════════════════════════════════════════════
// downloads
// ════════════════════════════════════════════════════════════════════

func TestCLI_Downloads_JSON_ServiceDown(t *testing.T) {
	stdout, _, code := run("downloads", "--output", "json")
	if code != 0 {
		t.Fatalf("downloads exited %d", code)
	}
	var errObj map[string]string
	var arr []interface{}
	if json.Unmarshal([]byte(stdout), &errObj) == nil {
		// qBittorrent down → error
	} else if json.Unmarshal([]byte(stdout), &arr) == nil {
		// qBittorrent up → array
	} else {
		t.Errorf("downloads JSON should be error or array, got: %s", stdout)
	}
}

// ════════════════════════════════════════════════════════════════════
// queue
// ════════════════════════════════════════════════════════════════════

func TestCLI_Queue_JSON(t *testing.T) {
	stdout, _, code := run("queue", "--output", "json")
	if code != 0 {
		t.Fatalf("queue exited %d", code)
	}
	var out interface{}
	if err := json.Unmarshal([]byte(stdout), &out); err != nil {
		t.Fatalf("queue JSON invalid: %v\nraw: %s", err, stdout)
	}
}

// ════════════════════════════════════════════════════════════════════
// missing
// ════════════════════════════════════════════════════════════════════

func TestCLI_Missing_JSON(t *testing.T) {
	stdout, _, code := run("missing", "--output", "json")
	if code != 0 {
		t.Fatalf("missing exited %d", code)
	}
	var out interface{}
	if err := json.Unmarshal([]byte(stdout), &out); err != nil {
		t.Fatalf("missing JSON invalid: %v\nraw: %s", err, stdout)
	}
}

// ════════════════════════════════════════════════════════════════════
// requests
// ════════════════════════════════════════════════════════════════════

func TestCLI_Requests_JSON(t *testing.T) {
	stdout, _, code := run("requests", "--output", "json")
	if code != 0 {
		t.Fatalf("requests exited %d", code)
	}
	var errObj map[string]string
	var arr []interface{}
	if json.Unmarshal([]byte(stdout), &errObj) == nil {
		// Seerr down
	} else if json.Unmarshal([]byte(stdout), &arr) == nil {
		// Seerr up
	} else {
		t.Errorf("requests JSON should be error or array, got: %s", stdout)
	}
}

// ════════════════════════════════════════════════════════════════════
// search (requires argument)
// ════════════════════════════════════════════════════════════════════

func TestCLI_Search_NoArg(t *testing.T) {
	_, stderr, code := run("search")
	if code == 0 {
		t.Fatal("search with no arg should fail")
	}
	if !strings.Contains(stderr, "arg") {
		t.Errorf("expected arg error, got: %s", stderr)
	}
}

func TestCLI_Search_JSON_ServiceDown(t *testing.T) {
	stdout, _, code := run("search", "test-query", "--output", "json")
	if code != 0 {
		t.Fatalf("search exited %d", code)
	}
	var out interface{}
	if err := json.Unmarshal([]byte(stdout), &out); err != nil {
		t.Fatalf("search JSON invalid: %v\nraw: %s", err, stdout)
	}
}

// ════════════════════════════════════════════════════════════════════
// find (requires argument)
// ════════════════════════════════════════════════════════════════════

func TestCLI_Find_NoArg(t *testing.T) {
	_, stderr, code := run("find")
	if code == 0 {
		t.Fatal("find with no arg should fail")
	}
	if !strings.Contains(stderr, "arg") {
		t.Errorf("expected arg error, got: %s", stderr)
	}
}

// ════════════════════════════════════════════════════════════════════
// logs (requires argument)
// ════════════════════════════════════════════════════════════════════

func TestCLI_Logs_NoArg(t *testing.T) {
	_, stderr, code := run("logs")
	if code == 0 {
		t.Fatal("logs with no arg should fail")
	}
	if !strings.Contains(stderr, "arg") {
		t.Errorf("expected arg error, got: %s", stderr)
	}
}

func TestCLI_Logs_JSON_ServiceDown(t *testing.T) {
	stdout, _, code := run("logs", "radarr", "--output", "json")
	if code != 0 {
		t.Fatalf("logs radarr exited %d", code)
	}
	var out interface{}
	if err := json.Unmarshal([]byte(stdout), &out); err != nil {
		t.Fatalf("logs JSON invalid: %v\nraw: %s", err, stdout)
	}
}

// ════════════════════════════════════════════════════════════════════
// restart (requires argument)
// ════════════════════════════════════════════════════════════════════

func TestCLI_Restart_NoArg(t *testing.T) {
	_, stderr, code := run("restart")
	if code == 0 {
		t.Fatal("restart with no arg should fail")
	}
	if !strings.Contains(stderr, "arg") {
		t.Errorf("expected arg error, got: %s", stderr)
	}
}

// ════════════════════════════════════════════════════════════════════
// completion
// ════════════════════════════════════════════════════════════════════

func TestCLI_Completion_Bash(t *testing.T) {
	stdout, _, code := run("completion", "bash")
	if code != 0 {
		t.Fatalf("completion bash exited %d", code)
	}
	if !strings.Contains(stdout, "bash completion") || !strings.Contains(stdout, "__admirarr") {
		t.Error("completion bash should output bash completion script")
	}
}

func TestCLI_Completion_Zsh(t *testing.T) {
	stdout, _, code := run("completion", "zsh")
	if code != 0 {
		t.Fatalf("completion zsh exited %d", code)
	}
	if !strings.Contains(stdout, "compdef") && !strings.Contains(stdout, "zsh") {
		t.Error("completion zsh should output zsh completion script")
	}
}

func TestCLI_Completion_Fish(t *testing.T) {
	stdout, _, code := run("completion", "fish")
	if code != 0 {
		t.Fatalf("completion fish exited %d", code)
	}
	if !strings.Contains(stdout, "complete") {
		t.Error("completion fish should output fish completion script")
	}
}

// ════════════════════════════════════════════════════════════════════
// Output format flag
// ════════════════════════════════════════════════════════════════════

func TestCLI_OutputFlag_JSON_ValidJSON(t *testing.T) {
	// Every command that supports --output json should produce valid JSON
	commands := [][]string{
		{"status"},
		{"health"},
		{"disk"},
		{"docker"},
		{"queue"},
		{"missing"},
	}

	for _, args := range commands {
		name := strings.Join(args, " ")
		t.Run(name, func(t *testing.T) {
			fullArgs := append(args, "--output", "json")
			stdout, _, code := run(fullArgs...)
			if code != 0 {
				t.Fatalf("%s -o json exited %d", name, code)
			}
			stdout = strings.TrimSpace(stdout)
			if stdout == "" {
				t.Fatalf("%s -o json produced empty output", name)
			}
			if !json.Valid([]byte(stdout)) {
				t.Errorf("%s -o json produced invalid JSON:\n%s", name, stdout[:min(200, len(stdout))])
			}
		})
	}
}

func TestCLI_OutputFlag_Text_NoBanner(t *testing.T) {
	// JSON mode should never show the text banner
	stdout, _, _ := run("status", "--output", "json")
	if strings.Contains(stdout, "⚓") || strings.Contains(stdout, "Command your fleet") {
		t.Error("JSON output should not contain text banner")
	}
}

// ════════════════════════════════════════════════════════════════════
// Edge cases
// ════════════════════════════════════════════════════════════════════

func TestCLI_DoubleFlag(t *testing.T) {
	// --output json --output json should not crash
	stdout, _, code := run("status", "--output", "json", "--output", "json")
	if code != 0 {
		t.Fatalf("double flag exited %d", code)
	}
	if !json.Valid([]byte(strings.TrimSpace(stdout))) {
		t.Error("double --output flag should still produce valid JSON")
	}
}

func TestCLI_InvalidOutputFormat(t *testing.T) {
	// --output xml should either error or fall back to text
	stdout, _, _ := run("status", "--output", "xml")
	// Should not crash — either shows text or errors gracefully
	if stdout == "" {
		t.Error("invalid output format should still produce some output")
	}
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
