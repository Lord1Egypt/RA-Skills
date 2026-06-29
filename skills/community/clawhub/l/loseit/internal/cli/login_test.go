package cli

import (
	"errors"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

// TestLoginCommandSavesToken runs the `login` command end-to-end against a fake
// Lose It login endpoint and asserts the returned cookie lands in the token file.
func TestLoginCommandSavesToken(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/account/login", func(w http.ResponseWriter, _ *http.Request) {
		http.SetCookie(w, &http.Cookie{Name: "liauth", Value: "TT"})
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte("{}"))
	})
	srv := httptest.NewServer(mux)
	defer srv.Close()

	tokenPath := filepath.Join(t.TempDir(), "token")
	t.Setenv("LOSEIT_TOKEN", "")
	t.Setenv("LOSEIT_LOGIN_URL", srv.URL+"/account/login")
	t.Setenv("LOSEIT_EMAIL", "user@example.com")
	t.Setenv("LOSEIT_PASSWORD", "pw")
	t.Setenv("LOSEIT_TOKEN_PATH", tokenPath)

	cfgPath := writeConfig(t, map[string]any{})
	stdout, _, err := run(t, "--config", cfgPath, "login")
	if err != nil {
		t.Fatalf("login: %v", err)
	}
	if !strings.Contains(stdout, "saved") {
		t.Errorf("stdout missing confirmation: %q", stdout)
	}
	b, err := os.ReadFile(tokenPath)
	if err != nil {
		t.Fatalf("token file: %v", err)
	}
	if strings.TrimSpace(string(b)) != "TT" {
		t.Errorf("token file = %q, want TT", strings.TrimSpace(string(b)))
	}
}

// TestLoginCommandBadCredentialsExits2 asserts a failed login maps to exit 2.
func TestLoginCommandBadCredentialsExits2(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/account/login", func(w http.ResponseWriter, _ *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		_, _ = w.Write([]byte(`{"error":"invalid_grant"}`))
	})
	srv := httptest.NewServer(mux)
	defer srv.Close()

	t.Setenv("LOSEIT_TOKEN", "")
	t.Setenv("LOSEIT_LOGIN_URL", srv.URL+"/account/login")
	t.Setenv("LOSEIT_EMAIL", "user@example.com")
	t.Setenv("LOSEIT_PASSWORD", "wrong")
	t.Setenv("LOSEIT_TOKEN_PATH", filepath.Join(t.TempDir(), "token"))

	cfgPath := writeConfig(t, map[string]any{})
	_, _, err := run(t, "--config", cfgPath, "login")
	var exit *ExitError
	if err == nil || !errors.As(err, &exit) || exit.Code != ExitExport {
		t.Fatalf("err = %v, want ExitError code %d", err, ExitExport)
	}
}
