// Package config resolves runtime configuration and credential discovery.
//
// Precedence (lowest to highest): built-in defaults < config.json < environment
// variables < command flags. The names of every env var and every JSON key are
// part of the external contract and must not be renamed — agents and scripts
// depend on them.
//
// This tool is a read-only Lose It! nutrition extractor: it obtains the export
// (a downloaded ZIP or a cookie fetch) and emits per-day nutrition. It knows
// nothing about any downstream data layout. There is intentionally no notion of
// a daily log here — the consuming agent stores whatever it cares about.
package config

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
)

// Environment variable names (frozen). G101: these are env-var names, not
// embedded credentials.
const (
	// User-facing credentials — the only inputs a normal user supplies.
	EnvEmail    = "LOSEIT_EMAIL"
	EnvPassword = "LOSEIT_PASSWORD" //nolint:gosec // env var name, not a secret.

	// Advanced/internal overrides — not user-facing. Retained for break-glass
	// fallbacks and tests (httptest servers point the URLs/token here); do not
	// remove any of them.
	EnvConfig    = "LOSEIT_CONFIG"
	EnvToken     = "LOSEIT_TOKEN" //nolint:gosec // env var name, not a secret.
	EnvTokenPath = "LOSEIT_TOKEN_PATH"
	EnvExportURL = "LOSEIT_EXPORT_URL"
	EnvLoginURL  = "LOSEIT_LOGIN_URL"
)

// Defaults.
const (
	DefaultTokenPath  = "~/.config/loseit/token"
	DefaultExportURL  = "https://www.loseit.com/export/data"
	DefaultLoginURL   = "https://api.loseit.com/account/login"
	defaultConfigName = "config.json"
)

// Config is the fully resolved configuration handed to commands.
type Config struct {
	// TokenPath is where the liauth session cookie is read from for the
	// cookie-fetch path. Kept as configured (may start with ~); the export layer
	// expands it at read time. The --zip path needs no token.
	TokenPath string
	// ExportURL is Lose It's first-party data-export endpoint.
	ExportURL string

	// Email and Password are the Lose It account credentials used by `login` to
	// obtain a fresh liauth cookie (mirroring speediance-cli). Optional: the
	// --zip path and a pre-saved token both work without them.
	Email    string
	Password string
	// LoginURL is Lose It's first-party password-grant login endpoint.
	LoginURL string

	// ConfigPath is where config.json was loaded from, or where it would be
	// written if it does not yet exist.
	ConfigPath string
	// ConfigExists reports whether ConfigPath was present on disk at load time.
	ConfigExists bool
}

// HasCredentials reports whether both email and password are set, so commands
// can decide whether auto-login is possible — without exposing the values.
func (c *Config) HasCredentials() bool { return c.Email != "" && c.Password != "" }

// fileConfig mirrors config.json. Pointer fields distinguish "key present" from
// "key absent" so an absent key falls through to the default rather than
// overwriting it with a zero value. Unknown keys (e.g. a stale daily_log from an
// older Python config) are ignored by encoding/json — a loose, forward-compatible
// decode.
type fileConfig struct {
	TokenPath *string `json:"token_path"`
	ExportURL *string `json:"export_url"`
	Email     *string `json:"email"`
	Password  *string `json:"password"`
	LoginURL  *string `json:"login_url"`
}

// Options carries inputs the caller already knows from flags, so config
// resolution can honor flag precedence without importing cobra.
type Options struct {
	// ConfigPath is the value of the --config flag (empty if not set). It wins
	// over LOSEIT_CONFIG when choosing which file to read.
	ConfigPath string
}

// Load resolves configuration from defaults, config.json, and environment
// variables. config.json is optional — the defaults work on their own.
func Load(opts Options) (*Config, error) {
	cfg := &Config{
		TokenPath: DefaultTokenPath,
		ExportURL: DefaultExportURL,
		LoginURL:  DefaultLoginURL,
	}

	// 1. Locate and read config.json (if any).
	path := discoverConfigPath(opts.ConfigPath)
	cfg.ConfigPath = path

	fc, exists, err := readFileConfig(path)
	if err != nil {
		return nil, err
	}
	cfg.ConfigExists = exists
	applyFile(cfg, fc)

	// 2. Environment overrides (LookupEnv distinguishes set-empty from unset).
	applyEnv(cfg)

	return cfg, nil
}

// discoverConfigPath implements config discovery:
//  1. --config flag or LOSEIT_CONFIG env (explicit path; flag wins).
//  2. config.json in the current working directory.
//  3. config.json next to the executable, so the tool works from any directory.
//  4. otherwise keep the CWD path (so `config show`/errors have something sane).
func discoverConfigPath(flagPath string) string {
	if flagPath != "" {
		return flagPath
	}
	if v, ok := os.LookupEnv(EnvConfig); ok && v != "" {
		return v
	}
	if _, err := os.Stat(defaultConfigName); err == nil {
		return defaultConfigName
	}
	if exe, err := os.Executable(); err == nil {
		alt := filepath.Join(filepath.Dir(exe), defaultConfigName)
		if _, err := os.Stat(alt); err == nil {
			return alt
		}
	}
	return defaultConfigName
}

func readFileConfig(path string) (fileConfig, bool, error) {
	var fc fileConfig
	data, err := os.ReadFile(path)
	if err != nil {
		if errors.Is(err, os.ErrNotExist) {
			return fc, false, nil
		}
		return fc, false, fmt.Errorf("read config %s: %w", path, err)
	}
	if err := json.Unmarshal(data, &fc); err != nil {
		return fc, true, fmt.Errorf("parse config %s: %w", path, err)
	}
	return fc, true, nil
}

func applyFile(cfg *Config, fc fileConfig) {
	if fc.TokenPath != nil {
		cfg.TokenPath = *fc.TokenPath
	}
	if fc.ExportURL != nil {
		cfg.ExportURL = *fc.ExportURL
	}
	if fc.Email != nil {
		cfg.Email = *fc.Email
	}
	if fc.Password != nil {
		cfg.Password = *fc.Password
	}
	if fc.LoginURL != nil {
		cfg.LoginURL = *fc.LoginURL
	}
}

func applyEnv(cfg *Config) {
	if v, ok := os.LookupEnv(EnvTokenPath); ok {
		cfg.TokenPath = v
	}
	if v, ok := os.LookupEnv(EnvExportURL); ok {
		cfg.ExportURL = v
	}
	if v, ok := os.LookupEnv(EnvEmail); ok {
		cfg.Email = v
	}
	if v, ok := os.LookupEnv(EnvPassword); ok {
		cfg.Password = v
	}
	if v, ok := os.LookupEnv(EnvLoginURL); ok {
		cfg.LoginURL = v
	}
}
