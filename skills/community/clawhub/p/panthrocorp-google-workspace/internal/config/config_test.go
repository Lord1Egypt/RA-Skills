package config

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
)

func TestDefaultConfig(t *testing.T) {
	cfg := DefaultConfig()
	if !cfg.Gmail {
		t.Error("expected gmail enabled by default")
	}
	if cfg.Calendar != ModeReadOnly {
		t.Errorf("expected calendar readonly by default, got %s", cfg.Calendar)
	}
	if !cfg.Contacts {
		t.Error("expected contacts enabled by default")
	}
	if cfg.Drive != ModeReadOnly {
		t.Errorf("expected drive readonly by default, got %s", cfg.Drive)
	}
	if cfg.Docs != ModeOff {
		t.Errorf("expected docs off by default, got %s", cfg.Docs)
	}
	if cfg.Sheets != ModeOff {
		t.Errorf("expected sheets off by default, got %s", cfg.Sheets)
	}
}

func TestValidate(t *testing.T) {
	tests := []struct {
		name    string
		cfg     Config
		wantErr bool
	}{
		{"all valid", Config{Gmail: true, Calendar: ModeReadOnly, Contacts: true, Drive: ModeReadOnly, Docs: ModeOff, Sheets: ModeOff}, false},
		{"all readwrite", Config{Gmail: true, Calendar: ModeReadWrite, Contacts: true, Drive: ModeReadWrite, Docs: ModeReadWrite, Sheets: ModeReadWrite}, false},
		{"all off", Config{Gmail: false, Calendar: ModeOff, Contacts: false, Drive: ModeOff, Docs: ModeOff, Sheets: ModeOff}, false},
		{"invalid calendar", Config{Calendar: ServiceMode("bogus")}, true},
		{"invalid drive", Config{Calendar: ModeOff, Drive: ServiceMode("bogus"), Docs: ModeOff, Sheets: ModeOff}, true},
		{"invalid docs", Config{Calendar: ModeOff, Drive: ModeOff, Docs: ServiceMode("bogus"), Sheets: ModeOff}, true},
		{"invalid sheets", Config{Calendar: ModeOff, Drive: ModeOff, Docs: ModeOff, Sheets: ServiceMode("bogus")}, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := tt.cfg.Validate()
			if (err != nil) != tt.wantErr {
				t.Errorf("Validate() error = %v, wantErr %v", err, tt.wantErr)
			}
		})
	}
}

func TestOAuthScopes(t *testing.T) {
	tests := []struct {
		name   string
		cfg    Config
		expect int
	}{
		{"all enabled readonly", Config{Gmail: true, Calendar: ModeReadOnly, Contacts: true, Drive: ModeReadOnly, Docs: ModeReadOnly, Sheets: ModeReadOnly}, 6},
		{"all enabled readwrite", Config{Gmail: true, Calendar: ModeReadWrite, Contacts: true, Drive: ModeReadWrite, Docs: ModeReadWrite, Sheets: ModeReadWrite}, 6},
		{"gmail only", Config{Gmail: true, Calendar: ModeOff, Contacts: false, Drive: ModeOff, Docs: ModeOff, Sheets: ModeOff}, 1},
		{"nothing", Config{Gmail: false, Calendar: ModeOff, Contacts: false, Drive: ModeOff, Docs: ModeOff, Sheets: ModeOff}, 0},
		{"calendar only", Config{Gmail: false, Calendar: ModeReadOnly, Contacts: false, Drive: ModeOff, Docs: ModeOff, Sheets: ModeOff}, 1},
		{"drive only", Config{Gmail: false, Calendar: ModeOff, Contacts: false, Drive: ModeReadOnly, Docs: ModeOff, Sheets: ModeOff}, 1},
		{"docs only", Config{Gmail: false, Calendar: ModeOff, Contacts: false, Drive: ModeOff, Docs: ModeReadOnly, Sheets: ModeOff}, 1},
		{"sheets only", Config{Gmail: false, Calendar: ModeOff, Contacts: false, Drive: ModeOff, Docs: ModeOff, Sheets: ModeReadOnly}, 1},
		{"default config", DefaultConfig(), 4},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			scopes := tt.cfg.OAuthScopes()
			if len(scopes) != tt.expect {
				t.Errorf("expected %d scopes, got %d: %v", tt.expect, len(scopes), scopes)
			}
		})
	}
}

func TestDriveScopeValues(t *testing.T) {
	readonly := Config{Drive: ModeReadOnly, Calendar: ModeOff, Docs: ModeOff, Sheets: ModeOff}
	readwrite := Config{Drive: ModeReadWrite, Calendar: ModeOff, Docs: ModeOff, Sheets: ModeOff}

	roScopes := readonly.OAuthScopes()
	if len(roScopes) != 1 || roScopes[0] != "https://www.googleapis.com/auth/drive.readonly" {
		t.Errorf("expected drive.readonly scope, got %v", roScopes)
	}

	rwScopes := readwrite.OAuthScopes()
	if len(rwScopes) != 1 || rwScopes[0] != "https://www.googleapis.com/auth/drive" {
		t.Errorf("expected full drive scope, got %v", rwScopes)
	}
}

func TestSaveAndLoad(t *testing.T) {
	dir := t.TempDir()

	cfg := Config{
		Gmail:    true,
		Calendar: ModeReadWrite,
		Contacts: false,
		Drive:    ModeReadWrite,
		Docs:     ModeReadOnly,
		Sheets:   ModeReadWrite,
	}

	if err := Save(dir, cfg); err != nil {
		t.Fatalf("Save: %v", err)
	}

	loaded, err := Load(dir)
	if err != nil {
		t.Fatalf("Load: %v", err)
	}

	if loaded != cfg {
		t.Errorf("loaded config does not match saved: got %+v, want %+v", loaded, cfg)
	}
}

func TestLoadMissing(t *testing.T) {
	dir := t.TempDir()
	cfg, err := Load(dir)
	if err != nil {
		t.Fatalf("Load: %v", err)
	}

	def := DefaultConfig()
	if cfg != def {
		t.Errorf("expected default config for missing file, got %+v", cfg)
	}
}

func TestLoadInvalid(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "config.json")
	if err := os.WriteFile(path, []byte(`{"calendar":"bogus"}`), 0o600); err != nil {
		t.Fatal(err)
	}

	_, err := Load(dir)
	if err == nil {
		t.Error("expected error loading invalid config")
	}
}

func TestLegacyDriveBoolTrue(t *testing.T) {
	data := []byte(`{"gmail":true,"calendar":"readonly","contacts":true,"drive":true}`)
	var cfg Config
	if err := json.Unmarshal(data, &cfg); err != nil {
		t.Fatalf("Unmarshal: %v", err)
	}
	if cfg.Drive != ModeReadOnly {
		t.Errorf("expected drive readonly for legacy true, got %s", cfg.Drive)
	}
}

func TestLegacyDriveBoolFalse(t *testing.T) {
	data := []byte(`{"gmail":true,"calendar":"readonly","contacts":true,"drive":false}`)
	var cfg Config
	if err := json.Unmarshal(data, &cfg); err != nil {
		t.Fatalf("Unmarshal: %v", err)
	}
	if cfg.Drive != ModeOff {
		t.Errorf("expected drive off for legacy false, got %s", cfg.Drive)
	}
}

func TestNewDriveStringMode(t *testing.T) {
	data := []byte(`{"gmail":true,"calendar":"readonly","contacts":true,"drive":"readwrite"}`)
	var cfg Config
	if err := json.Unmarshal(data, &cfg); err != nil {
		t.Fatalf("Unmarshal: %v", err)
	}
	if cfg.Drive != ModeReadWrite {
		t.Errorf("expected drive readwrite, got %s", cfg.Drive)
	}
}

func TestMissingDocsSheets(t *testing.T) {
	data := []byte(`{"gmail":true,"calendar":"readonly","contacts":true,"drive":"readonly"}`)
	var cfg Config
	if err := json.Unmarshal(data, &cfg); err != nil {
		t.Fatalf("Unmarshal: %v", err)
	}
	if cfg.Docs != ModeOff {
		t.Errorf("expected docs off for missing field, got %s", cfg.Docs)
	}
	if cfg.Sheets != ModeOff {
		t.Errorf("expected sheets off for missing field, got %s", cfg.Sheets)
	}
}

func TestLegacyConfigRoundTrip(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "config.json")

	legacy := []byte(`{"gmail":true,"calendar":"readonly","contacts":true,"drive":true}`)
	if err := os.WriteFile(path, legacy, 0o600); err != nil {
		t.Fatal(err)
	}

	cfg, err := Load(dir)
	if err != nil {
		t.Fatalf("Load legacy: %v", err)
	}
	if cfg.Drive != ModeReadOnly {
		t.Errorf("expected drive readonly after loading legacy, got %s", cfg.Drive)
	}

	if err := Save(dir, cfg); err != nil {
		t.Fatalf("Save: %v", err)
	}

	reloaded, err := Load(dir)
	if err != nil {
		t.Fatalf("Reload: %v", err)
	}
	if reloaded.Drive != ModeReadOnly {
		t.Errorf("expected drive readonly after round-trip, got %s", reloaded.Drive)
	}
}
