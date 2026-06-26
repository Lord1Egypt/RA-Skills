package cmd

import (
	"testing"
)

func TestRootCommand_HasSubcommands(t *testing.T) {
	cmds := rootCmd.Commands()
	if len(cmds) == 0 {
		t.Fatal("root command should have subcommands registered")
	}

	// Build a set of registered command names
	registered := make(map[string]bool)
	for _, c := range cmds {
		registered[c.Name()] = true
	}

	// Verify critical commands exist
	required := []string{
		"setup", "doctor", "status", "health",
		"restart", "downloads", "movies", "shows",
		"search", "queue", "indexers", "migrate",
	}
	for _, name := range required {
		if !registered[name] {
			t.Errorf("expected command %q to be registered", name)
		}
	}
}

func TestSetupCommand_Metadata(t *testing.T) {
	if setupCmd.Use != "setup" {
		t.Errorf("expected Use=setup, got %s", setupCmd.Use)
	}
	if setupCmd.Short == "" {
		t.Error("setup command should have a short description")
	}
	if setupCmd.Long == "" {
		t.Error("setup command should have a long description")
	}
	if setupCmd.Example == "" {
		t.Error("setup command should have an example")
	}
}

func TestDoctorCommand_Metadata(t *testing.T) {
	if doctorCmd.Use != "doctor" {
		t.Errorf("expected Use=doctor, got %s", doctorCmd.Use)
	}
	if setupCmd.Short == "" {
		t.Error("doctor command should have a short description")
	}

	// Check --fix flag exists
	flag := doctorCmd.Flags().Lookup("fix")
	if flag == nil {
		t.Error("doctor command should have --fix flag")
	}
}

func TestStatusCommand_Metadata(t *testing.T) {
	if statusCmd.Use != "status" {
		t.Errorf("expected Use=status, got %s", statusCmd.Use)
	}

	// Check --live flag exists
	flag := statusCmd.Flags().Lookup("live")
	if flag == nil {
		t.Error("status command should have --live flag")
	}

	// Check --interval flag exists
	flag = statusCmd.Flags().Lookup("interval")
	if flag == nil {
		t.Error("status command should have --interval flag")
	}
}

func TestFmtETA(t *testing.T) {
	tests := []struct {
		secs     int64
		expected string
	}{
		{0, ""},
		{-1, ""},
		{8640001, ""},       // > 100 days
		{30, "30s"},
		{59, "59s"},
		{60, "1m0s"},
		{90, "1m30s"},
		{3599, "59m59s"},
		{3600, "1h0m"},
		{3661, "1h1m"},
		{7200, "2h0m"},
	}
	for _, tt := range tests {
		got := fmtETA(tt.secs)
		if got != tt.expected {
			t.Errorf("fmtETA(%d) = %q, want %q", tt.secs, got, tt.expected)
		}
	}
}

func TestRootCommand_VersionSet(t *testing.T) {
	if rootCmd.Version == "" {
		t.Error("root command should have a version set")
	}
}

func TestAllCommandsHaveShortDescription(t *testing.T) {
	for _, cmd := range rootCmd.Commands() {
		if cmd.Short == "" {
			t.Errorf("command %q missing short description", cmd.Name())
		}
	}
}

func TestHealthCommand_Exists(t *testing.T) {
	registered := make(map[string]bool)
	for _, c := range rootCmd.Commands() {
		registered[c.Name()] = true
	}
	if !registered["health"] {
		t.Error("health command should be registered")
	}
}

func TestRestartCommand_Exists(t *testing.T) {
	registered := make(map[string]bool)
	for _, c := range rootCmd.Commands() {
		registered[c.Name()] = true
	}
	if !registered["restart"] {
		t.Error("restart command should be registered")
	}
}
