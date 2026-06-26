package setup

import (
	"strings"
	"testing"

	"github.com/maxtechera/admirarr/internal/arr"
)

func TestStepResult_Pass(t *testing.T) {
	r := StepResult{Name: "Test"}
	r.pass()
	r.pass()
	if r.Passed != 2 {
		t.Errorf("expected 2 passed, got %d", r.Passed)
	}
}

func TestStepResult_Fix(t *testing.T) {
	r := StepResult{Name: "Test"}
	r.fix()
	if r.Fixed != 1 {
		t.Errorf("expected 1 fixed, got %d", r.Fixed)
	}
}

func TestStepResult_Skip(t *testing.T) {
	r := StepResult{Name: "Test"}
	r.skip()
	r.skip()
	r.skip()
	if r.Skipped != 3 {
		t.Errorf("expected 3 skipped, got %d", r.Skipped)
	}
}

func TestStepResult_Err(t *testing.T) {
	r := StepResult{Name: "Test"}
	r.err("something broke")
	if len(r.Errors) != 1 {
		t.Fatalf("expected 1 error, got %d", len(r.Errors))
	}
	if r.Errors[0] != "something broke" {
		t.Errorf("unexpected error message: %s", r.Errors[0])
	}
}

func TestStepResult_Errf(t *testing.T) {
	r := StepResult{Name: "Test"}
	r.errf("service %s: %s", "radarr", "timeout")
	if len(r.Errors) != 1 {
		t.Fatalf("expected 1 error, got %d", len(r.Errors))
	}
	if r.Errors[0] != "service radarr: timeout" {
		t.Errorf("unexpected error: %s", r.Errors[0])
	}
}

func TestStepResult_Combined(t *testing.T) {
	r := StepResult{Name: "Combined"}
	r.pass()
	r.pass()
	r.fix()
	r.skip()
	r.err("fail1")
	r.errf("fail%d", 2)

	if r.Passed != 2 || r.Fixed != 1 || r.Skipped != 1 || len(r.Errors) != 2 {
		t.Errorf("unexpected result: %+v", r)
	}
}

func TestMaskKey(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"abcdefghijklmnop", "abcd…mnop"},
		{"short", "****"},
		{"12345678", "****"},
		{"123456789", "1234…6789"},
	}
	for _, tt := range tests {
		got := maskKey(tt.input)
		if got != tt.expected {
			t.Errorf("maskKey(%q) = %q, want %q", tt.input, got, tt.expected)
		}
	}
}

func TestBuildYAML_BasicOutput(t *testing.T) {
	state := &SetupState{
		DataPath: "/data",
		Services: map[string]*ServiceState{
			"radarr": {Port: 7878, Detected: true},
			"seerr":  {Port: 5055, Detected: true},
		},
		SelectedServices: []string{"radarr", "seerr"},
		Keys:             make(map[string]string),
		ManualKeys:       make(map[string]string),
	}

	yaml := buildYAML(state)

	if !strings.Contains(yaml, `data_path: "/data"`) {
		t.Errorf("expected data_path in YAML, got:\n%s", yaml)
	}
	if !strings.Contains(yaml, "radarr:") {
		t.Errorf("expected radarr service in YAML, got:\n%s", yaml)
	}
	if !strings.Contains(yaml, "host: localhost") {
		t.Errorf("expected host: localhost in YAML, got:\n%s", yaml)
	}
}

func TestBuildYAML_ManualKeysIncluded(t *testing.T) {
	state := &SetupState{
		DataPath: "/data",
		Services: map[string]*ServiceState{},
		Keys:     map[string]string{"radarr": "auto-key"},
		ManualKeys: map[string]string{
			"sonarr": "manual-key-123",
		},
	}

	yaml := buildYAML(state)

	if !strings.Contains(yaml, "keys:") {
		t.Error("expected keys section")
	}
	if !strings.Contains(yaml, `sonarr: "manual-key-123"`) {
		t.Error("expected manual sonarr key in YAML")
	}
	// Auto-discovered keys should also be in the YAML (persisted for convenience)
	if !strings.Contains(yaml, `radarr: "auto-key"`) {
		t.Error("auto-discovered keys should be in YAML")
	}
}

func TestBuildYAML_AlwaysHasKeysSection(t *testing.T) {
	state := &SetupState{
		DataPath:   "/data",
		Services:   map[string]*ServiceState{},
		Keys:       make(map[string]string),
		ManualKeys: make(map[string]string),
	}

	yaml := buildYAML(state)

	if !strings.Contains(yaml, "keys:") {
		t.Error("expected keys section in YAML output")
	}
}

func TestBuildYAML_DockerHostLocalhost(t *testing.T) {
	state := &SetupState{
		DataPath: "/data",
		Services: map[string]*ServiceState{
			"seerr": {Port: 5055, Detected: true},
		},
		SelectedServices: []string{"seerr"},
		Keys:             make(map[string]string),
		ManualKeys:       make(map[string]string),
	}

	yaml := buildYAML(state)

	if !strings.Contains(yaml, "host: localhost") {
		t.Errorf("expected service to have host localhost in YAML:\n%s", yaml)
	}
}

func TestBuildYAML_ComposeDirAndTimezone(t *testing.T) {
	state := &SetupState{
		DataPath:   "/data",
		ComposeDir: "/home/user/docker",
		Timezone:   "America/New_York",
		Services:   map[string]*ServiceState{},
		Keys:       make(map[string]string),
		ManualKeys: make(map[string]string),
	}

	yaml := buildYAML(state)

	if !strings.Contains(yaml, `compose_dir: "/home/user/docker"`) {
		t.Errorf("expected compose_dir in YAML, got:\n%s", yaml)
	}
	if !strings.Contains(yaml, `timezone: "America/New_York"`) {
		t.Errorf("expected timezone in YAML, got:\n%s", yaml)
	}
}

func TestBuildYAML_OnlyDetectedServices(t *testing.T) {
	state := &SetupState{
		DataPath: "/data",
		Services: map[string]*ServiceState{
			"radarr": {Port: 7878, Detected: true},
			"sonarr": {Port: 8989, Detected: false, Reachable: false},
		},
		SelectedServices: []string{"radarr", "sonarr"},
		Keys:             make(map[string]string),
		ManualKeys:       make(map[string]string),
	}

	yaml := buildYAML(state)

	if !strings.Contains(yaml, "radarr:") {
		t.Errorf("expected radarr in YAML (detected), got:\n%s", yaml)
	}
	// sonarr should not appear in the services section (it's in keys section as empty)
	if strings.Contains(yaml, "  sonarr:\n    port:") {
		t.Errorf("sonarr should NOT be in services section (not detected/reachable), got:\n%s", yaml)
	}
}

func TestDownloadClient_GetSetField(t *testing.T) {
	dc := arr.DownloadClient{
		Fields: []arr.DownloadClientField{
			{Name: "host", Value: "localhost"},
			{Name: "port", Value: 8080},
		},
	}

	// Get existing field
	if v := dc.GetField("host"); v != "localhost" {
		t.Errorf("expected host=localhost, got %v", v)
	}

	// Get non-existent field
	if v := dc.GetField("missing"); v != nil {
		t.Errorf("expected nil for missing field, got %v", v)
	}

	// Set existing field
	dc.SetField("host", "192.168.1.1")
	if v := dc.GetField("host"); v != "192.168.1.1" {
		t.Errorf("expected updated host, got %v", v)
	}

	// Set new field
	dc.SetField("username", "admin")
	if v := dc.GetField("username"); v != "admin" {
		t.Errorf("expected username=admin, got %v", v)
	}
	if len(dc.Fields) != 3 {
		t.Errorf("expected 3 fields, got %d", len(dc.Fields))
	}
}

func TestSetupState_Init(t *testing.T) {
	state := &SetupState{
		Services:   make(map[string]*ServiceState),
		Keys:       make(map[string]string),
		ManualKeys: make(map[string]string),
	}

	if state.Services == nil || state.Keys == nil || state.ManualKeys == nil {
		t.Error("maps should not be nil after init")
	}

	// Add a service and verify
	state.Services["radarr"] = &ServiceState{
		Detected:  true,
		Reachable: true,
		IsDocker:  true,
		Host:      "localhost",
		Port:      7878,
		APIKey:    "test-key",
	}

	svc := state.Services["radarr"]
	if !svc.Detected || !svc.Reachable || svc.Port != 7878 || !svc.IsDocker {
		t.Errorf("unexpected service state: %+v", svc)
	}
}

func TestSetupState_InternalURL(t *testing.T) {
	state := &SetupState{
		Services: map[string]*ServiceState{
			"radarr": {IsDocker: true, Port: 7878},
			"sonarr": {IsDocker: false, Port: 8989},
		},
	}

	// Docker service uses container name
	got := state.InternalURL("radarr")
	if got != "http://radarr:7878" {
		t.Errorf("expected http://radarr:7878, got %s", got)
	}

	// Native service uses localhost
	got = state.InternalURL("sonarr")
	if got != "http://localhost:8989" {
		t.Errorf("expected http://localhost:8989, got %s", got)
	}
}
