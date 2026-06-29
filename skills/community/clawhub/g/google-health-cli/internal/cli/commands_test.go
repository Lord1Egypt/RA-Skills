package cli

import (
	"bytes"
	"encoding/json"
	"errors"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"golang.org/x/oauth2"

	"github.com/stozo04/google-health-cli/internal/auth"
	"github.com/stozo04/google-health-cli/internal/config"
)

// fixtureServer serves the committed exercise fixture for any request.
func fixtureServer(t *testing.T) *httptest.Server {
	t.Helper()
	body, err := os.ReadFile(filepath.Join("..", "..", "testdata", "fixtures", "exercise_all.json"))
	if err != nil {
		t.Fatalf("read fixture: %v", err)
	}
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write(body)
	}))
	t.Cleanup(srv.Close)
	return srv
}

// withBaseURL points the API client at url for the duration of the test.
func withBaseURL(t *testing.T, url string) {
	t.Helper()
	prev := baseURLOverride
	baseURLOverride = url
	t.Cleanup(func() { baseURLOverride = prev })
}

// testConfig writes a config.json and (optionally) a valid token into a temp
// dir, returning the config path.
func testConfig(t *testing.T, withToken bool) string {
	t.Helper()
	dir := t.TempDir()
	tokenPath := filepath.Join(dir, "token.json")
	cfgPath := filepath.Join(dir, "config.json")

	cfg := map[string]any{
		"client_id":     "test-client",
		"client_secret": "test-secret",
		"token_cache":   tokenPath,
	}
	b, _ := json.Marshal(cfg)
	if err := os.WriteFile(cfgPath, b, 0o600); err != nil {
		t.Fatal(err)
	}
	if withToken {
		tok := &oauth2.Token{AccessToken: "fake", TokenType: "Bearer", Expiry: time.Now().Add(24 * time.Hour)}
		if err := auth.SaveToken(tokenPath, tok); err != nil {
			t.Fatal(err)
		}
	}
	return cfgPath
}

// run executes the root command with args, capturing stdout and stderr.
func run(t *testing.T, args ...string) (stdout, stderr string, err error) {
	t.Helper()
	root := NewRootCmd()
	var out, errBuf bytes.Buffer
	root.SetOut(&out)
	root.SetErr(&errBuf)
	root.SetArgs(args)
	err = root.Execute()
	return out.String(), errBuf.String(), err
}

func TestSessionsJSONCommand(t *testing.T) {
	srv := fixtureServer(t)
	withBaseURL(t, srv.URL)
	cfg := testConfig(t, true)

	stdout, _, err := run(t, "--config", cfg, "sessions", "--json", "--date", "2026-06-16", "--days", "60")
	if err != nil {
		t.Fatalf("sessions: %v", err)
	}
	assertGolden(t, "sessions_json.golden", []byte(stdout))
}

func TestSessionsRawCommand(t *testing.T) {
	srv := fixtureServer(t)
	withBaseURL(t, srv.URL)
	cfg := testConfig(t, true)

	stdout, _, err := run(t, "--config", cfg, "sessions", "--raw", "--date", "2026-06-16", "--days", "60")
	if err != nil {
		t.Fatalf("sessions --raw: %v", err)
	}
	assertGolden(t, "sessions_raw.golden", []byte(stdout))
}

func TestSessionsNotAuthenticated(t *testing.T) {
	cfg := testConfig(t, false) // no token
	_, _, err := run(t, "--config", cfg, "sessions")
	var exit *ExitError
	if !errors.As(err, &exit) || exit.Code != ExitAuth {
		t.Fatalf("err = %v, want ExitError code 2", err)
	}
}

func TestDataListCommand(t *testing.T) {
	srv := fixtureServer(t)
	withBaseURL(t, srv.URL)
	cfg := testConfig(t, true)

	// The fixture server returns the exercise payload for any path; `data list
	// exercise` should emit a JSON array on stdout and a count on stderr.
	stdout, stderr, err := run(t, "--config", cfg, "data", "list", "exercise", "--date", "2026-06-16", "--days", "60")
	if err != nil {
		t.Fatalf("data list: %v", err)
	}
	var arr []json.RawMessage
	if err := json.Unmarshal([]byte(stdout), &arr); err != nil {
		t.Fatalf("data list stdout not a JSON array: %v\n%s", err, stdout)
	}
	if len(arr) == 0 {
		t.Error("expected data points from the fixture")
	}
	if !strings.Contains(stderr, "exercise data point(s)") {
		t.Errorf("stderr missing count hint: %q", stderr)
	}
}

func TestDataListUnknownTypeIsUsageError(t *testing.T) {
	cfg := testConfig(t, true)
	_, _, err := run(t, "--config", cfg, "data", "list", "not-a-type")
	var exit *ExitError
	if !errors.As(err, &exit) || exit.Code != ExitUsage {
		t.Fatalf("err = %v, want ExitError code %d", err, ExitUsage)
	}
}

// TestAPIGetRejectsNonV4PathAsUsageError guards that the `api get` escape hatch's
// path validation surfaces as a usage error (exit 64), not an auth/API failure,
// and (implicitly) that a non-v4 path never reaches the network. Pairs with
// api.TestRawGet_RejectsPathsOutsideV4Surface, which proves the no-network claim.
func TestAPIGetRejectsNonV4PathAsUsageError(t *testing.T) {
	cfg := testConfig(t, true) // valid token, so we get past auth to path validation
	for _, path := range []string{"/v3/users/me", "http://evil.example/v4/x", "/admin"} {
		_, _, err := run(t, "--config", cfg, "api", "get", path)
		var exit *ExitError
		if !errors.As(err, &exit) || exit.Code != ExitUsage {
			t.Errorf("api get %q: err = %v, want ExitError code %d", path, err, ExitUsage)
		}
	}
}

// TestDataEmittingCommandsWarnAtRuntime is the immutable guard for the
// "missing user warnings" runtime finding: every command that prints personal
// health data must emit the execution-time privacy notice to stderr (and never to
// stdout, which is machine-readable data). Removing emitPrivacyNotice from any
// data-emitting command fails this. Fix by restoring the call, never by deleting
// the test.
func TestDataEmittingCommandsWarnAtRuntime(t *testing.T) {
	cfg := testConfig(t, true)

	check := func(t *testing.T, stdout, stderr string) {
		t.Helper()
		if !strings.Contains(stderr, privacyNotice) {
			t.Errorf("stderr missing runtime privacy notice; got: %q", stderr)
		}
		if strings.Contains(stdout, privacyNotice) {
			t.Error("privacy notice leaked onto stdout (must be stderr only — stdout is data)")
		}
	}

	t.Run("data list", func(t *testing.T) {
		srv := fixtureServer(t)
		withBaseURL(t, srv.URL)
		stdout, stderr, err := run(t, "--config", cfg, "data", "list", "exercise", "--date", "2026-06-16", "--days", "60")
		if err != nil {
			t.Fatalf("data list: %v", err)
		}
		check(t, stdout, stderr)
	})

	t.Run("sessions", func(t *testing.T) {
		srv := fixtureServer(t)
		withBaseURL(t, srv.URL)
		stdout, stderr, err := run(t, "--config", cfg, "sessions", "--json", "--date", "2026-06-16", "--days", "60")
		if err != nil {
			t.Fatalf("sessions: %v", err)
		}
		check(t, stdout, stderr)
	})

	t.Run("rollup daily", func(t *testing.T) {
		srv, _ := rollupFixtureServer(t)
		withBaseURL(t, srv.URL)
		stdout, stderr, err := run(t, "--config", cfg, "rollup", "daily", "steps", "--date", "2026-06-16", "--days", "2")
		if err != nil {
			t.Fatalf("rollup daily: %v", err)
		}
		check(t, stdout, stderr)
	})

	t.Run("api get", func(t *testing.T) {
		srv := fixtureServer(t)
		withBaseURL(t, srv.URL)
		stdout, stderr, err := run(t, "--config", cfg, "api", "get", "/v4/users/me/profile")
		if err != nil {
			t.Fatalf("api get: %v", err)
		}
		check(t, stdout, stderr)
	})
}

func TestTypesListJSON(t *testing.T) {
	stdout, _, err := run(t, "types", "list", "--json")
	if err != nil {
		t.Fatalf("types list: %v", err)
	}
	var views []map[string]any
	if err := json.Unmarshal([]byte(stdout), &views); err != nil {
		t.Fatalf("types list --json not valid JSON: %v", err)
	}
	if len(views) != 31 {
		t.Errorf("types list returned %d, want 31", len(views))
	}
}

func TestDoctorValidToken(t *testing.T) {
	cfg := testConfig(t, true)
	stdout, _, err := run(t, "--config", cfg, "doctor")
	if err != nil {
		t.Fatalf("doctor: %v", err)
	}
	var report doctorReport
	if err := json.Unmarshal([]byte(stdout), &report); err != nil {
		t.Fatalf("doctor JSON: %v\n%s", err, stdout)
	}
	if !report.TokenValid {
		t.Error("tokenValid = false, want true for a fresh token")
	}
	if !report.ConfigFound {
		t.Error("configFound = false, want true when --config points at a real file")
	}
	if !report.ClientIDLoaded {
		t.Error("clientIdLoaded = false, want true when the config carries client_id")
	}
}

func TestDoctorReportsMissingConfig(t *testing.T) {
	// --config points at a nonexistent file: doctor must flag configFound:false /
	// clientIdLoaded:false, warn naming the search order, and exit non-zero —
	// instead of printing a relative configPath and exiting 0 (issue #6, AC #3).
	missing := filepath.Join(t.TempDir(), "nope.json")
	stdout, stderr, err := run(t, "--config", missing, "doctor")
	var exit *ExitError
	if !errors.As(err, &exit) || exit.Code != ExitConfig {
		t.Fatalf("err = %v, want exit %d", err, ExitConfig)
	}
	var report doctorReport
	if jerr := json.Unmarshal([]byte(stdout), &report); jerr != nil {
		t.Fatalf("doctor JSON: %v\n%s", jerr, stdout)
	}
	if report.ConfigFound {
		t.Error("configFound = true, want false for a nonexistent config")
	}
	if report.ClientIDLoaded {
		t.Error("clientIdLoaded = true, want false with no config")
	}
	if !strings.Contains(stderr, "No config found") || !strings.Contains(stderr, "client_id") {
		t.Errorf("stderr not actionable: %q", stderr)
	}
}

func TestDoctorReportsConfigWithoutCredentials(t *testing.T) {
	// A config that exists but lacks client_id/client_secret: configFound true,
	// clientIdLoaded false, with a distinct warning and a non-zero exit.
	dir := t.TempDir()
	cfgPath := filepath.Join(dir, "config.json")
	if err := os.WriteFile(cfgPath, []byte(`{"user":"users/me"}`), 0o600); err != nil {
		t.Fatal(err)
	}
	stdout, stderr, err := run(t, "--config", cfgPath, "doctor")
	var exit *ExitError
	if !errors.As(err, &exit) || exit.Code != ExitConfig {
		t.Fatalf("err = %v, want exit %d", err, ExitConfig)
	}
	var report doctorReport
	if jerr := json.Unmarshal([]byte(stdout), &report); jerr != nil {
		t.Fatalf("doctor JSON: %v", jerr)
	}
	if !report.ConfigFound {
		t.Error("configFound = false, want true for an existing file")
	}
	if report.ClientIDLoaded {
		t.Error("clientIdLoaded = true, want false without client_id")
	}
	if !strings.Contains(stderr, "missing client_id/client_secret") {
		t.Errorf("stderr missing credential warning: %q", stderr)
	}
}

func TestAPICommandFailsFastWithoutCredentials(t *testing.T) {
	// Expired token + a config without client credentials: an API command must
	// fail fast with exit 64 and an actionable message naming the discovery
	// order — NOT the raw oauth2 "Could not determine client ID" string
	// (issue #6, AC #1).
	dir := t.TempDir()
	tokenPath := filepath.Join(dir, "token.json")
	cfgPath := filepath.Join(dir, "config.json")
	b, _ := json.Marshal(map[string]any{"token_cache": tokenPath}) // no client_id/secret
	if err := os.WriteFile(cfgPath, b, 0o600); err != nil {
		t.Fatal(err)
	}
	expired := &oauth2.Token{
		AccessToken:  "stale",
		RefreshToken: "refresh",
		TokenType:    "Bearer",
		Expiry:       time.Now().Add(-time.Hour),
	}
	if err := auth.SaveToken(tokenPath, expired); err != nil {
		t.Fatal(err)
	}

	_, _, err := run(t, "--config", cfgPath, "data", "list", "steps", "--days", "1")
	var exit *ExitError
	if !errors.As(err, &exit) || exit.Code != ExitUsage {
		t.Fatalf("err = %v, want exit %d", err, ExitUsage)
	}
	if strings.Contains(err.Error(), "Could not determine client ID") {
		t.Errorf("leaked raw oauth2 error: %v", err)
	}
	if !strings.Contains(err.Error(), "client_id") || !strings.Contains(err.Error(), "Looked at") {
		t.Errorf("error not actionable: %v", err)
	}
}

func TestValidTokenWorksWithoutCredentials(t *testing.T) {
	// AC #5: a still-valid cached token needs no client credentials, so the fast
	// path must keep working even when the config carries no client_id/secret.
	srv := fixtureServer(t)
	withBaseURL(t, srv.URL)

	dir := t.TempDir()
	tokenPath := filepath.Join(dir, "token.json")
	cfgPath := filepath.Join(dir, "config.json")
	b, _ := json.Marshal(map[string]any{"token_cache": tokenPath}) // no client_id/secret
	if err := os.WriteFile(cfgPath, b, 0o600); err != nil {
		t.Fatal(err)
	}
	valid := &oauth2.Token{AccessToken: "fresh", TokenType: "Bearer", Expiry: time.Now().Add(24 * time.Hour)}
	if err := auth.SaveToken(tokenPath, valid); err != nil {
		t.Fatal(err)
	}

	if _, _, err := run(t, "--config", cfgPath, "data", "list", "exercise", "--date", "2026-06-16", "--days", "60"); err != nil {
		t.Fatalf("valid token + no creds should still succeed: %v", err)
	}
}

func TestDoctorNotAuthenticatedExits2(t *testing.T) {
	cfg := testConfig(t, false)
	stdout, stderr, err := run(t, "--config", cfg, "doctor")
	var exit *ExitError
	if !errors.As(err, &exit) || exit.Code != ExitAuth {
		t.Fatalf("err = %v, want exit 2", err)
	}
	var report doctorReport
	if jerr := json.Unmarshal([]byte(stdout), &report); jerr != nil {
		t.Fatalf("doctor still prints JSON: %v", jerr)
	}
	if report.TokenValid {
		t.Error("tokenValid = true, want false")
	}
	if !strings.Contains(stderr, "auth login") {
		t.Errorf("stderr missing hint: %q", stderr)
	}
}

func TestAuthStatusJSON(t *testing.T) {
	cfg := testConfig(t, true)
	stdout, _, err := run(t, "--config", cfg, "auth", "status", "--json")
	if err != nil {
		t.Fatalf("auth status: %v", err)
	}
	var report authStatusReport
	if err := json.Unmarshal([]byte(stdout), &report); err != nil {
		t.Fatalf("auth status JSON: %v", err)
	}
	if !report.Present || !report.Valid {
		t.Errorf("present/valid = %v/%v, want true/true", report.Present, report.Valid)
	}
}

func TestAuthLogout(t *testing.T) {
	cfg := testConfig(t, true)
	if _, _, err := run(t, "--config", cfg, "auth", "logout"); err != nil {
		t.Fatalf("auth logout: %v", err)
	}
	// A subsequent status should report no token.
	stdout, _, err := run(t, "--config", cfg, "auth", "status", "--json")
	if err != nil {
		t.Fatal(err)
	}
	var report authStatusReport
	_ = json.Unmarshal([]byte(stdout), &report)
	if report.Present {
		t.Error("token still present after logout")
	}
}

func TestEndToEndMigratesLegacyTokenToCacheDir(t *testing.T) {
	// CLI conventions §1+§7, end-to-end: a token at the legacy <UserConfigDir>
	// default is relocated to the <UserCacheDir> default through the real command
	// tree (resolveConfig), with the session preserved. Hermetic across OSes —
	// every base dir Go consults is overridden so the real user dirs are untouched.
	t.Chdir(t.TempDir())
	configBase, cacheBase, home := t.TempDir(), t.TempDir(), t.TempDir()
	t.Setenv("XDG_CONFIG_HOME", configBase) // Linux config base
	t.Setenv("XDG_CACHE_HOME", cacheBase)   // Linux cache base
	t.Setenv("AppData", configBase)         // Windows %AppData% (config base)
	t.Setenv("LocalAppData", cacheBase)     // Windows %LocalAppData% (cache base)
	t.Setenv("HOME", home)                  // macOS ~/Library/* base
	// Neutralize inherited overrides so the defaults are used (migration only runs
	// for the default path).
	t.Setenv(config.EnvConfig, "")
	t.Setenv(config.EnvTokenCache, "")

	legacy := config.LegacyTokenCachePath()
	if legacy == "" {
		t.Skip("no user config dir resolvable on this platform")
	}
	cfg, err := config.Load(config.Options{})
	if err != nil {
		t.Fatalf("Load: %v", err)
	}
	newPath := cfg.TokenCache
	if newPath == legacy {
		t.Fatalf("new (%s) and legacy token paths coincide — cannot prove relocation", newPath)
	}

	tok := &oauth2.Token{AccessToken: "live", RefreshToken: "r", TokenType: "Bearer", Expiry: time.Now().Add(24 * time.Hour)}
	if err := auth.SaveToken(legacy, tok); err != nil {
		t.Fatal(err)
	}

	// Any command through the tree triggers resolveConfig, which performs the move.
	if _, _, rerr := run(t, "config", "path"); rerr != nil {
		t.Fatalf("config path: %v", rerr)
	}

	if got, _ := auth.LoadToken(legacy); got != nil {
		t.Errorf("legacy token still present at %s after migration", legacy)
	}
	moved, err := auth.LoadToken(newPath)
	if err != nil || moved == nil {
		t.Fatalf("token not found at new cache path %s: %v", newPath, err)
	}
	if moved.AccessToken != "live" {
		t.Errorf("relocated token AccessToken = %q, want live (session not preserved)", moved.AccessToken)
	}
}
