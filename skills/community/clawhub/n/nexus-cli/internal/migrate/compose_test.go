package migrate

import (
	"strings"
	"testing"
)

func TestGenerateCompose_Header(t *testing.T) {
	out := GenerateCompose([]string{"radarr"}, ComposeOpts{
		DataDir:   "/data",
		ConfigDir: "/config",
		TZ:        "UTC",
		PUID:      "1000",
		PGID:      "1000",
	})

	if !strings.HasPrefix(out, "# Admirarr Docker Compose Stack") {
		t.Error("compose output should start with header comment")
	}
	if !strings.Contains(out, "services:") {
		t.Error("compose output should contain services: key")
	}
}

func TestGenerateCompose_IncludesSelectedServices(t *testing.T) {
	services := []string{"radarr", "sonarr", "prowlarr"}
	out := GenerateCompose(services, ComposeOpts{
		DataDir:   "/data",
		ConfigDir: "/config",
		TZ:        "UTC",
		PUID:      "1000",
		PGID:      "1000",
	})

	for _, svc := range services {
		if !strings.Contains(out, "container_name: "+svc) {
			t.Errorf("expected compose to contain %s service", svc)
		}
	}
}

func TestGenerateCompose_ExcludesUnselectedServices(t *testing.T) {
	out := GenerateCompose([]string{"radarr"}, ComposeOpts{
		DataDir:   "/data",
		ConfigDir: "/config",
		TZ:        "UTC",
		PUID:      "1000",
		PGID:      "1000",
	})

	if strings.Contains(out, "container_name: sonarr") {
		t.Error("compose should not contain unselected services")
	}
}

func TestGenerateCompose_EnvHintComment(t *testing.T) {
	out := GenerateCompose([]string{"radarr"}, ComposeOpts{
		DataDir:   "/data",
		ConfigDir: "/config",
		TZ:        "America/New_York",
		PUID:      "1000",
		PGID:      "1000",
	})

	if !strings.Contains(out, "# DATA_DIR=/data") {
		t.Error("compose should contain DATA_DIR env hint")
	}
	if !strings.Contains(out, "# TZ=America/New_York") {
		t.Error("compose should contain TZ env hint")
	}
}

func TestGenerateCompose_VPNHint(t *testing.T) {
	out := GenerateCompose([]string{"gluetun"}, ComposeOpts{
		DataDir:     "/data",
		ConfigDir:   "/config",
		TZ:          "UTC",
		PUID:        "1000",
		PGID:        "1000",
		VPNProvider: "mullvad",
		VPNType:     "wireguard",
	})

	if !strings.Contains(out, "# VPN_PROVIDER=mullvad") {
		t.Error("compose should contain VPN_PROVIDER hint when set")
	}
}

func TestGenerateCompose_UnknownServiceSkipped(t *testing.T) {
	out := GenerateCompose([]string{"radarr", "nonexistent"}, ComposeOpts{
		DataDir:   "/data",
		ConfigDir: "/config",
		TZ:        "UTC",
		PUID:      "1000",
		PGID:      "1000",
	})

	if !strings.Contains(out, "container_name: radarr") {
		t.Error("known service should still be included")
	}
	if strings.Contains(out, "nonexistent") {
		t.Error("unknown service should be silently skipped")
	}
}

func TestGenerateEnvFile_ContainsAllVars(t *testing.T) {
	out := GenerateEnvFile(ComposeOpts{
		DataDir:   "/data",
		ConfigDir: "/config",
		TZ:        "UTC",
		PUID:      "1000",
		PGID:      "1000",
	}, "")

	expected := []string{
		"DATA_DIR=/data",
		"CONFIG_DIR=/config",
		"TZ=UTC",
		"PUID=1000",
		"PGID=1000",
	}
	for _, line := range expected {
		if !strings.Contains(out, line) {
			t.Errorf("expected .env to contain %q", line)
		}
	}
}

func TestGenerateEnvFile_VPNVars(t *testing.T) {
	out := GenerateEnvFile(ComposeOpts{
		DataDir:     "/data",
		ConfigDir:   "/config",
		TZ:          "UTC",
		PUID:        "1000",
		PGID:        "1000",
		VPNProvider: "mullvad",
		VPNType:     "wireguard",
	}, "")

	if !strings.Contains(out, "VPN_PROVIDER=mullvad") {
		t.Error("expected VPN_PROVIDER in .env")
	}
	if !strings.Contains(out, "VPN_TYPE=wireguard") {
		t.Error("expected VPN_TYPE in .env")
	}
}

func TestGenerateEnvFile_NoVPN(t *testing.T) {
	out := GenerateEnvFile(ComposeOpts{
		DataDir:   "/data",
		ConfigDir: "/config",
		TZ:        "UTC",
		PUID:      "1000",
		PGID:      "1000",
	}, "")

	if strings.Contains(out, "VPN_PROVIDER") {
		t.Error("should not contain VPN vars when not set")
	}
}

func TestOrderServices_GluetunBeforeQbittorrent(t *testing.T) {
	ordered := orderServices([]string{"qbittorrent", "radarr", "gluetun"})

	gluetunIdx := -1
	qbtIdx := -1
	for i, s := range ordered {
		if s == "gluetun" {
			gluetunIdx = i
		}
		if s == "qbittorrent" {
			qbtIdx = i
		}
	}

	if gluetunIdx == -1 {
		t.Fatal("gluetun should be in ordered list")
	}
	if qbtIdx == -1 {
		t.Fatal("qbittorrent should be in ordered list")
	}
	if gluetunIdx >= qbtIdx {
		t.Errorf("gluetun (idx %d) should come before qbittorrent (idx %d)", gluetunIdx, qbtIdx)
	}
}

func TestOrderServices_AddsGluetunWhenQbittorrentSelected(t *testing.T) {
	ordered := orderServices([]string{"qbittorrent", "radarr"})

	has := make(map[string]bool)
	for _, s := range ordered {
		has[s] = true
	}

	if !has["gluetun"] {
		t.Error("gluetun should be auto-added when qbittorrent is selected")
	}
}

func TestOrderServices_NoGluetunWithoutQbittorrent(t *testing.T) {
	ordered := orderServices([]string{"radarr", "sonarr"})

	for _, s := range ordered {
		if s == "gluetun" {
			t.Error("gluetun should not be added when qbittorrent is not selected")
		}
	}
}

func TestOrderServices_PreservesAllServices(t *testing.T) {
	input := []string{"sonarr", "radarr", "prowlarr", "bazarr"}
	ordered := orderServices(input)

	has := make(map[string]bool)
	for _, s := range ordered {
		has[s] = true
	}

	for _, s := range input {
		if !has[s] {
			t.Errorf("service %s missing from ordered output", s)
		}
	}
}
