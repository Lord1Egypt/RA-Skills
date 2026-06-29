// Package config resolves runtime configuration and credential discovery.
//
// Precedence (lowest to highest): built-in defaults < config.json < environment
// variables < command flags. The names of every env var and every JSON key are
// part of the external contract and must not be renamed — agents and scripts
// depend on them.
//
// This tool is a generic, read-only Google Health extractor: it owns OAuth and
// the v4 API wire, and knows nothing about any downstream data layout. There is
// intentionally no notion of a daily log, an exercise allowlist, or heart-rate
// bands here — consuming agents derive whatever they care about from the emitted
// data.
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
	EnvConfig       = "GOOGLE_HEALTH_CONFIG"
	EnvClientID     = "GOOGLE_HEALTH_CLIENT_ID"
	EnvClientSecret = "GOOGLE_HEALTH_CLIENT_SECRET" //nolint:gosec // env var name, not a secret.
	EnvBaseURL      = "GOOGLE_HEALTH_BASE_URL"
	EnvTokenCache   = "GOOGLE_HEALTH_TOKEN_CACHE"
)

// Defaults.
const (
	DefaultBaseURL = "https://health.googleapis.com"
	DefaultUser    = "users/me"

	defaultConfigName = "config.json"
	defaultTokenName  = "token.json"
	appDirName        = "google-health-cli"
)

// DefaultScopes is the full set of read-only Google Health scopes the tool
// requests at login, so an authorized token can read every data type the API
// exposes. Read-only only — the tool never requests a write scope.
var DefaultScopes = []string{
	"https://www.googleapis.com/auth/googlehealth.profile.readonly",
	"https://www.googleapis.com/auth/googlehealth.settings.readonly",
	"https://www.googleapis.com/auth/googlehealth.activity_and_fitness.readonly",
	"https://www.googleapis.com/auth/googlehealth.health_metrics_and_measurements.readonly",
	"https://www.googleapis.com/auth/googlehealth.sleep.readonly",
	"https://www.googleapis.com/auth/googlehealth.nutrition.readonly",
}

// Config is the fully resolved configuration handed to commands.
type Config struct {
	ClientID     string
	ClientSecret string
	BaseURL      string
	User         string
	TokenCache   string
	Scopes       []string

	// ConfigPath is where config.json was loaded from, or where it would be
	// written if it does not yet exist.
	ConfigPath string
	// ConfigExists reports whether ConfigPath was present on disk at load time.
	ConfigExists bool
	// SearchedPaths lists, in priority order, the discovery locations consulted
	// to find config.json. It is the single source of truth for the "looked at"
	// hint in diagnostics (doctor) and the fail-fast error, so the message can
	// never drift from the real search order.
	SearchedPaths []string
	// TokenCacheIsDefault reports that TokenCache fell through to the built-in
	// default (no --config/file/env override). Only then is it safe to migrate a
	// token forward from a previous default location (shared CLI conventions §7).
	TokenCacheIsDefault bool
}

// HasOAuthClient reports whether both OAuth client credentials are loaded. A
// token refresh needs both; without them an expired token cannot be refreshed
// and Google's token endpoint returns a cryptic "Could not determine client ID"
// error. Callers use this to fail fast with an actionable message instead.
func (c *Config) HasOAuthClient() bool {
	return c.ClientID != "" && c.ClientSecret != ""
}

// fileConfig mirrors config.json. Pointer fields distinguish "key present" from
// "key absent" so an absent key falls through to the default rather than
// overwriting it with a zero value. Unknown keys (e.g. a stale daily_log or
// elliptical_types from an older config) are ignored by encoding/json — a loose,
// forward-compatible decode.
type fileConfig struct {
	ClientID     *string  `json:"client_id"`
	ClientSecret *string  `json:"client_secret"`
	BaseURL      *string  `json:"base_url"`
	User         *string  `json:"user"`
	TokenCache   *string  `json:"token_cache"`
	Scopes       []string `json:"scopes"`
}

// Options carries inputs the caller already knows from flags, so config
// resolution can honor flag precedence without importing cobra.
type Options struct {
	// ConfigPath is the value of the --config flag (empty if not set). It wins
	// over GOOGLE_HEALTH_CONFIG when choosing which file to read.
	ConfigPath string
}

// Load resolves configuration from defaults, config.json, and environment
// variables.
func Load(opts Options) (*Config, error) {
	cfg := &Config{
		BaseURL: DefaultBaseURL,
		User:    DefaultUser,
		Scopes:  append([]string(nil), DefaultScopes...),
	}

	// 1. Locate and read config.json (if any).
	path, searched := discoverConfigPath(opts.ConfigPath)
	cfg.ConfigPath = path
	cfg.SearchedPaths = searched

	fc, exists, err := readFileConfig(path)
	if err != nil {
		return nil, err
	}
	cfg.ConfigExists = exists
	applyFile(cfg, fc)

	// 2. Environment overrides (LookupEnv distinguishes set-empty from unset).
	applyEnv(cfg)

	// 3. Token cache location: flag/file/env override, else the non-roaming
	// per-user default (<UserCacheDir>/app/token.json). When the default is used,
	// flag it so the caller may migrate a token forward from the old location.
	if cfg.TokenCache == "" {
		cfg.TokenCache = defaultTokenCachePath()
		cfg.TokenCacheIsDefault = true
	}

	return cfg, nil
}

// discoverConfigPath implements config discovery, returning the chosen path and
// the ordered list of locations it consulted (for diagnostics and the "no config
// found" hint):
//  1. --config flag or GOOGLE_HEALTH_CONFIG env (explicit path; flag wins).
//  2. config.json in the current working directory.
//  3. config.json next to the executable, so the tool works from any directory.
//  4. config.json in the user config dir, next to the token cache, so the tool
//     works from any directory with neither --config nor the env var set.
//  5. otherwise keep the CWD path (so `config show`/errors have something sane).
func discoverConfigPath(flagPath string) (path string, searched []string) {
	if flagPath != "" {
		return flagPath, []string{"--config " + flagPath}
	}
	searched = append(searched, "$"+EnvConfig)
	if v, ok := os.LookupEnv(EnvConfig); ok && v != "" {
		return v, searched
	}
	searched = append(searched, "./"+defaultConfigName+" (current directory)")
	if _, err := os.Stat(defaultConfigName); err == nil {
		return defaultConfigName, searched
	}
	if exe, err := os.Executable(); err == nil {
		alt := filepath.Join(filepath.Dir(exe), defaultConfigName)
		searched = append(searched, alt+" (next to the executable)")
		if _, err := os.Stat(alt); err == nil {
			return alt, searched
		}
	}
	if appCfg := appConfigPath(); appCfg != "" {
		searched = append(searched, appCfg+" (user config dir)")
		if _, err := os.Stat(appCfg); err == nil {
			return appCfg, searched
		}
	}
	return defaultConfigName, searched
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
	if fc.ClientID != nil {
		cfg.ClientID = *fc.ClientID
	}
	if fc.ClientSecret != nil {
		cfg.ClientSecret = *fc.ClientSecret
	}
	if fc.BaseURL != nil {
		cfg.BaseURL = *fc.BaseURL
	}
	if fc.User != nil {
		cfg.User = *fc.User
	}
	if fc.TokenCache != nil {
		cfg.TokenCache = *fc.TokenCache
	}
	if fc.Scopes != nil {
		cfg.Scopes = fc.Scopes
	}
}

func applyEnv(cfg *Config) {
	if v, ok := os.LookupEnv(EnvClientID); ok {
		cfg.ClientID = v
	}
	if v, ok := os.LookupEnv(EnvClientSecret); ok {
		cfg.ClientSecret = v
	}
	if v, ok := os.LookupEnv(EnvBaseURL); ok {
		cfg.BaseURL = v
	}
	if v, ok := os.LookupEnv(EnvTokenCache); ok {
		cfg.TokenCache = v
	}
}

// userConfigDir and userCacheDir wrap the os equivalents, indirected so tests can
// point discovery at temp dirs instead of the developer's real ~/.config,
// ~/.cache, %AppData%, or %LocalAppData%.
var (
	userConfigDir = os.UserConfigDir
	userCacheDir  = os.UserCacheDir
)

// defaultTokenCachePath is <UserCacheDir>/google-health-cli/token.json. The token
// is regenerable state, not config, so it lives under the non-roaming cache base
// (Windows %LocalAppData%) rather than UserConfigDir (%AppData%\Roaming, which
// syncs a live credential across machines). Falls back to ./token.json only if
// the cache dir can't be determined. See .claude/CLI_CONVENTIONS.md §1.
func defaultTokenCachePath() string {
	if dir, err := userCacheDir(); err == nil {
		return filepath.Join(dir, appDirName, defaultTokenName)
	}
	return defaultTokenName
}

// LegacyTokenCachePath is the pre-relocation default (<UserConfigDir>/
// google-health-cli/token.json). It is exposed only so the CLI can migrate an
// existing token forward to defaultTokenCachePath; "" if it can't be determined.
func LegacyTokenCachePath() string {
	if dir, err := userConfigDir(); err == nil {
		return filepath.Join(dir, appDirName, defaultTokenName)
	}
	return ""
}

// appConfigPath is <UserConfigDir>/google-health-cli/config.json — the config
// sibling of the token cache — or "" if the user config dir can't be determined.
func appConfigPath() string {
	if dir, err := userConfigDir(); err == nil {
		return filepath.Join(dir, appDirName, defaultConfigName)
	}
	return ""
}
