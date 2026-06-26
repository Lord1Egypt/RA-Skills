package config

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/spf13/viper"
)

// loadClean resets viper and loads with no config file by pointing HOME to a temp dir.
func loadClean(t *testing.T) {
	t.Helper()
	viper.Reset()
	cfg = nil
	dir := t.TempDir()
	t.Setenv("HOME", dir)
	Load()
}

func TestLoad_Defaults(t *testing.T) {
	loadClean(t)

	if Host() != "localhost" {
		t.Errorf("expected default host localhost, got %s", Host())
	}
	if DataPath() != "/data" {
		t.Errorf("expected default data_path /data, got %s", DataPath())
	}
}

func TestLoad_FromFile(t *testing.T) {
	viper.Reset()
	cfg = nil

	dir := t.TempDir()
	configFile := filepath.Join(dir, "config.yaml")
	content := `data_path: "/media"
services:
  radarr:
    port: 7878
    api_ver: "v3"
  sonarr:
    port: 8989
    api_ver: "v3"
keys:
  radarr: "test-radarr-key"
`
	os.WriteFile(configFile, []byte(content), 0644)

	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath(dir)

	Load()

	if DataPath() != "/media" {
		t.Errorf("expected data_path /media, got %s", DataPath())
	}
	if ManualKey("radarr") != "test-radarr-key" {
		t.Errorf("expected radarr key, got %s", ManualKey("radarr"))
	}
}

func TestLoad_ExplicitHost(t *testing.T) {
	viper.Reset()
	cfg = nil

	dir := t.TempDir()
	content := `host: "10.0.0.5"
services:
  radarr:
    host: "10.0.0.5"
    port: 7878
  sonarr:
    port: 8989
  seerr:
    host: localhost
    port: 5055
`
	os.WriteFile(filepath.Join(dir, "config.yaml"), []byte(content), 0644)

	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath(dir)
	Load()

	// Service with explicit host uses it
	if h := ServiceHost("radarr"); h != "10.0.0.5" {
		t.Errorf("radarr: expected host 10.0.0.5, got %s", h)
	}
	// Service without explicit host defaults to localhost
	if h := ServiceHost("sonarr"); h != "localhost" {
		t.Errorf("sonarr: expected host localhost, got %s", h)
	}
	// Service with explicit localhost keeps it
	if h := ServiceHost("seerr"); h != "localhost" {
		t.Errorf("seerr: expected host localhost, got %s", h)
	}
}

func TestLoad_IsConfigured(t *testing.T) {
	viper.Reset()
	cfg = nil

	dir := t.TempDir()
	content := `services:
  radarr:
    port: 7878
`
	os.WriteFile(filepath.Join(dir, "config.yaml"), []byte(content), 0644)

	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath(dir)
	Load()

	if !IsConfigured("radarr") {
		t.Error("radarr should be configured")
	}
	if IsConfigured("lidarr") {
		t.Error("lidarr should not be configured")
	}
}

func TestAllServiceNames_HasCoreServices(t *testing.T) {
	names := AllServiceNames()
	required := []string{"jellyfin", "radarr", "sonarr", "prowlarr", "qbittorrent"}
	nameSet := make(map[string]bool)
	for _, n := range names {
		nameSet[n] = true
	}
	for _, r := range required {
		if !nameSet[r] {
			t.Errorf("expected %s in AllServiceNames(), got %v", r, names)
		}
	}
}

func TestDefaultServices_Ports(t *testing.T) {
	expectedPorts := map[string]int{
		"jellyfin": 8096, "qbittorrent": 8080, "prowlarr": 9696,
		"sonarr": 8989, "radarr": 7878, "seerr": 5055,
		"bazarr": 6767, "flaresolverr": 8191,
		"lidarr": 8686, "readarr": 8787, "whisparr": 6969,
	}
	for name, expectedPort := range expectedPorts {
		def, ok := GetServiceDef(name)
		if !ok {
			t.Errorf("%s not found in registry", name)
			continue
		}
		if def.Port != expectedPort {
			t.Errorf("%s: expected port %d, got %d", name, expectedPort, def.Port)
		}
	}
}

func TestServiceAPIVer(t *testing.T) {
	loadClean(t)

	if v := ServiceAPIVer("radarr"); v != "v3" {
		t.Errorf("radarr: expected v3, got %s", v)
	}
	if v := ServiceAPIVer("sonarr"); v != "v3" {
		t.Errorf("sonarr: expected v3, got %s", v)
	}
	if v := ServiceAPIVer("prowlarr"); v != "v1" {
		t.Errorf("prowlarr: expected v1, got %s", v)
	}
	if v := ServiceAPIVer("lidarr"); v != "v1" {
		t.Errorf("lidarr: expected v1, got %s", v)
	}
}

func TestServiceURL_Format(t *testing.T) {
	loadClean(t)

	url := ServiceURL("radarr")
	expected := "http://localhost:7878"
	if url != expected {
		t.Errorf("expected %s, got %s", expected, url)
	}
}

func TestAllServices_UseLocalhost_WithNoConfig(t *testing.T) {
	loadClean(t)

	// With no config file, all services should default to localhost
	for _, name := range AllServiceNames() {
		host := ServiceHost(name)
		if host != "localhost" {
			t.Errorf("%s: expected host=localhost, got %s", name, host)
		}
	}
}

func TestIndexerConfig_IsEnabled(t *testing.T) {
	trueVal := true
	falseVal := false

	tests := []struct {
		name     string
		ic       IndexerConfig
		expected bool
	}{
		{"nil defaults to true", IndexerConfig{Enabled: nil}, true},
		{"explicit true", IndexerConfig{Enabled: &trueVal}, true},
		{"explicit false", IndexerConfig{Enabled: &falseVal}, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.ic.IsEnabled(); got != tt.expected {
				t.Errorf("expected %v, got %v", tt.expected, got)
			}
		})
	}
}

func TestContainerName(t *testing.T) {
	tests := map[string]string{
		"jellyfin": "jellyfin",
		"seerr":    "seerr",
		"radarr":   "radarr",
		"lidarr":   "lidarr",
		"unknown":  "unknown", // fallback to service name
	}
	for svc, expected := range tests {
		got := ContainerName(svc)
		if got != expected {
			t.Errorf("ContainerName(%q) = %q, want %q", svc, got, expected)
		}
	}
}
