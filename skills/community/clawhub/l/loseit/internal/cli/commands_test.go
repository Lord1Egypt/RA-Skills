package cli

import (
	"bytes"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stozo04/loseit-cli/internal/config"
)

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

// writeConfig writes a config.json into a temp dir and returns its path.
func writeConfig(t *testing.T, cfg map[string]any) string {
	t.Helper()
	dir := t.TempDir()
	path := filepath.Join(dir, "config.json")
	b, _ := json.Marshal(cfg)
	if err := os.WriteFile(path, b, 0o600); err != nil {
		t.Fatal(err)
	}
	return path
}

// normalizeLF strips carriage returns so Windows checkouts compare byte-for-byte
// against the LF goldens.
func normalizeLF(b []byte) []byte {
	return bytes.ReplaceAll(b, []byte("\r"), nil)
}

func assertGolden(t *testing.T, name string, got []byte) {
	t.Helper()
	path := filepath.Join("..", "..", "testdata", "golden", name)
	// UPDATE_GOLDEN=1 rewrites the golden from the current output (goldens are
	// stored LF).
	if os.Getenv("UPDATE_GOLDEN") != "" {
		if err := os.WriteFile(path, normalizeLF(got), 0o644); err != nil {
			t.Fatalf("update golden %s: %v", name, err)
		}
		return
	}
	want, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("read golden %s: %v", name, err)
	}
	g, w := normalizeLF(got), normalizeLF(want)
	if !bytes.Equal(g, w) {
		t.Errorf("output does not match golden %s\n--- got (%d bytes) ---\n%s\n--- want (%d bytes) ---\n%s",
			name, len(g), g, len(w), w)
	}
}

func TestVersionJSON(t *testing.T) {
	stdout, _, err := run(t, "version", "--json")
	if err != nil {
		t.Fatalf("version: %v", err)
	}
	var info map[string]any
	if err := json.Unmarshal([]byte(stdout), &info); err != nil {
		t.Fatalf("version --json not valid JSON: %v\n%s", err, stdout)
	}
	for _, k := range []string{"version", "commit", "date", "go"} {
		if _, ok := info[k]; !ok {
			t.Errorf("version JSON missing key %q", k)
		}
	}
}

func TestConfigShowJSONDefaults(t *testing.T) {
	cfgPath := writeConfig(t, map[string]any{}) // empty file → defaults apply.
	stdout, _, err := run(t, "--config", cfgPath, "config", "show", "--json")
	if err != nil {
		t.Fatalf("config show: %v", err)
	}
	var view map[string]any
	if err := json.Unmarshal([]byte(stdout), &view); err != nil {
		t.Fatalf("config show --json invalid: %v", err)
	}
	if view["export_url"] != config.DefaultExportURL {
		t.Errorf("export_url = %v, want %s", view["export_url"], config.DefaultExportURL)
	}
	if view["token_path"] != config.DefaultTokenPath {
		t.Errorf("token_path = %v, want %s", view["token_path"], config.DefaultTokenPath)
	}
}

func TestDoctorNoTokenExitsZeroWithHint(t *testing.T) {
	t.Setenv(config.EnvToken, "") // ensure no env token.
	missing := filepath.Join(t.TempDir(), "absent-token")
	cfgPath := writeConfig(t, map[string]any{"token_path": missing})

	stdout, stderr, err := run(t, "--config", cfgPath, "doctor")
	if err != nil {
		t.Fatalf("doctor should exit 0 without a token, got: %v", err)
	}
	var report map[string]any
	if err := json.Unmarshal([]byte(stdout), &report); err != nil {
		t.Fatalf("doctor JSON invalid: %v\n%s", err, stdout)
	}
	if report["tokenPresent"] != false {
		t.Errorf("tokenPresent = %v, want false", report["tokenPresent"])
	}
	if !strings.Contains(stderr, "No Lose It token") {
		t.Errorf("stderr missing hint: %q", stderr)
	}
}

func TestDoctorWithTokenPresent(t *testing.T) {
	t.Setenv(config.EnvToken, "liauth-cookie")
	cfgPath := writeConfig(t, map[string]any{})
	stdout, _, err := run(t, "--config", cfgPath, "doctor")
	if err != nil {
		t.Fatalf("doctor: %v", err)
	}
	var report map[string]any
	if err := json.Unmarshal([]byte(stdout), &report); err != nil {
		t.Fatal(err)
	}
	if report["tokenPresent"] != true {
		t.Errorf("tokenPresent = %v, want true", report["tokenPresent"])
	}
}

// TestConfigShowNeverRevealsPassword pins that the password is never emitted by
// `config show`, in either the human or --json form — only the password_set
// boolean. Regressing this (e.g. adding a password field to configView, or
// printing the value) fails the test.
func TestConfigShowNeverRevealsPassword(t *testing.T) {
	const secret = "super-secret-pw-DO-NOT-LEAK"
	cfgPath := writeConfig(t, map[string]any{"email": "you@example.com", "password": secret})

	stdout, _, err := run(t, "--config", cfgPath, "config", "show")
	if err != nil {
		t.Fatalf("config show: %v", err)
	}
	if strings.Contains(stdout, secret) {
		t.Errorf("config show leaked the password:\n%s", stdout)
	}

	jstdout, _, err := run(t, "--config", cfgPath, "config", "show", "--json")
	if err != nil {
		t.Fatalf("config show --json: %v", err)
	}
	if strings.Contains(jstdout, secret) {
		t.Errorf("config show --json leaked the password:\n%s", jstdout)
	}
	var view map[string]any
	if err := json.Unmarshal([]byte(jstdout), &view); err != nil {
		t.Fatalf("config show --json invalid: %v", err)
	}
	if view["password_set"] != true {
		t.Errorf("password_set = %v, want true", view["password_set"])
	}
	if _, ok := view["password"]; ok {
		t.Error("config show --json must not include a password field")
	}
}

// TestDoctorNeverRevealsTokenOrPassword pins that doctor reports presence as
// booleans without ever echoing the token value or password to stdout/stderr.
func TestDoctorNeverRevealsTokenOrPassword(t *testing.T) {
	const token = "liauth-secret-cookie-value-DO-NOT-LEAK"
	const pw = "doctor-secret-pw-DO-NOT-LEAK"
	t.Setenv(config.EnvToken, token)
	cfgPath := writeConfig(t, map[string]any{"email": "you@example.com", "password": pw})

	stdout, stderr, err := run(t, "--config", cfgPath, "doctor")
	if err != nil {
		t.Fatalf("doctor: %v", err)
	}
	for label, s := range map[string]string{"stdout": stdout, "stderr": stderr} {
		if strings.Contains(s, token) {
			t.Errorf("doctor leaked the token value on %s:\n%s", label, s)
		}
		if strings.Contains(s, pw) {
			t.Errorf("doctor leaked the password on %s:\n%s", label, s)
		}
	}
	var report map[string]any
	if err := json.Unmarshal([]byte(stdout), &report); err != nil {
		t.Fatalf("doctor JSON invalid: %v", err)
	}
	if report["tokenPresent"] != true || report["credentialsPresent"] != true {
		t.Errorf("doctor presence flags = %v, want both true", report)
	}
}

func TestCompletionBash(t *testing.T) {
	stdout, _, err := run(t, "completion", "bash")
	if err != nil {
		t.Fatalf("completion bash: %v", err)
	}
	if !strings.Contains(stdout, "loseit-cli") {
		t.Error("bash completion output does not mention loseit-cli")
	}
}
