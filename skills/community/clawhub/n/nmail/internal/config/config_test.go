package config

import (
	"os"
	"path/filepath"
	"testing"
)

func TestProviderPresets(t *testing.T) {
	naver, ok := ProviderPresets[ProviderNaver]
	if !ok {
		t.Fatal("naver preset missing")
	}
	if naver.IMAPHost != "imap.naver.com" {
		t.Errorf("naver IMAP host = %q, want imap.naver.com", naver.IMAPHost)
	}
	if naver.IMAPPort != 993 {
		t.Errorf("naver IMAP port = %d, want 993", naver.IMAPPort)
	}
	if naver.SMTPHost != "smtp.naver.com" {
		t.Errorf("naver SMTP host = %q, want smtp.naver.com", naver.SMTPHost)
	}

	daum, ok := ProviderPresets[ProviderDaum]
	if !ok {
		t.Fatal("daum preset missing")
	}
	if daum.IMAPPort != 993 {
		t.Errorf("daum IMAP port = %d, want 993", daum.IMAPPort)
	}
}

func TestConfigAddAndDefault(t *testing.T) {
	cfg := &Config{}

	acct := Account{
		Name:     "test",
		Email:    "test@naver.com",
		Password: "pw",
		Provider: ProviderNaver,
		IMAPHost: "imap.naver.com",
		IMAPPort: 993,
		IMAPTLS:  true,
		SMTPHost: "smtp.naver.com",
		SMTPPort: 587,
	}
	cfg.Add(acct)

	if len(cfg.Accounts) != 1 {
		t.Fatalf("accounts = %d, want 1", len(cfg.Accounts))
	}
	if cfg.DefaultAccount != "test@naver.com" {
		t.Errorf("default = %q, want test@naver.com", cfg.DefaultAccount)
	}

	def, err := cfg.Default()
	if err != nil {
		t.Fatalf("Default() error: %v", err)
	}
	if def.Email != "test@naver.com" {
		t.Errorf("default email = %q", def.Email)
	}
}

func TestConfigAddUpdate(t *testing.T) {
	cfg := &Config{}
	cfg.Add(Account{Email: "a@naver.com", Name: "old"})
	cfg.Add(Account{Email: "a@naver.com", Name: "new"})

	if len(cfg.Accounts) != 1 {
		t.Fatalf("accounts = %d, want 1 (update, not duplicate)", len(cfg.Accounts))
	}
	if cfg.Accounts[0].Name != "new" {
		t.Errorf("name = %q, want new", cfg.Accounts[0].Name)
	}
}

func TestConfigRemove(t *testing.T) {
	cfg := &Config{}
	cfg.Add(Account{Email: "a@naver.com"})
	cfg.Add(Account{Email: "b@daum.net"})

	if !cfg.Remove("a@naver.com") {
		t.Error("Remove returned false for existing account")
	}
	if len(cfg.Accounts) != 1 {
		t.Fatalf("accounts = %d, want 1", len(cfg.Accounts))
	}
	if cfg.Accounts[0].Email != "b@daum.net" {
		t.Error("wrong account remained")
	}

	if cfg.Remove("nonexistent@test.com") {
		t.Error("Remove returned true for non-existent account")
	}
}

func TestConfigDefaultEmpty(t *testing.T) {
	cfg := &Config{}
	_, err := cfg.Default()
	if err == nil {
		t.Error("expected error for empty config")
	}
}

func TestSaveAndLoad(t *testing.T) {
	// Use temp dir to avoid touching real config
	tmpDir := t.TempDir()
	origHome := os.Getenv("HOME")
	os.Setenv("HOME", tmpDir)
	defer os.Setenv("HOME", origHome)

	cfg := &Config{}
	cfg.Add(Account{
		Email:    "test@naver.com",
		Provider: ProviderNaver,
		IMAPHost: "imap.naver.com",
		IMAPPort: 993,
	})

	if err := Save(cfg); err != nil {
		t.Fatalf("Save error: %v", err)
	}

	// Verify file exists
	path := filepath.Join(tmpDir, ".nmail", "config.yaml")
	if _, err := os.Stat(path); os.IsNotExist(err) {
		t.Fatal("config file not created")
	}

	loaded, err := Load()
	if err != nil {
		t.Fatalf("Load error: %v", err)
	}
	if len(loaded.Accounts) != 1 {
		t.Fatalf("loaded accounts = %d, want 1", len(loaded.Accounts))
	}
	if loaded.Accounts[0].Email != "test@naver.com" {
		t.Errorf("loaded email = %q", loaded.Accounts[0].Email)
	}
}

func TestLoadNonExistent(t *testing.T) {
	tmpDir := t.TempDir()
	origHome := os.Getenv("HOME")
	os.Setenv("HOME", tmpDir)
	defer os.Setenv("HOME", origHome)

	cfg, err := Load()
	if err != nil {
		t.Fatalf("Load error for non-existent: %v", err)
	}
	if len(cfg.Accounts) != 0 {
		t.Error("expected empty config")
	}
}
