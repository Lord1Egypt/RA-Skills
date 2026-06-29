package export

import (
	"context"
	"crypto/rand"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"testing"

	"github.com/stozo04/loseit-cli/internal/config"
)

const goodToken = "LIAUTH_TEST_TOKEN"

// bigZip returns a valid ZIP guaranteed to clear FetchZip's >1000-byte check by
// bundling a high-entropy blob that won't compress away.
func bigZip(t *testing.T) []byte {
	t.Helper()
	blob := make([]byte, 4096)
	if _, err := rand.Read(blob); err != nil {
		t.Fatal(err)
	}
	return makeZip(t, map[string]string{
		FoodLogsCSV: "Date,Name,Calories\n2026-06-16,Greek Yogurt,120\n",
		"blob.bin":  string(blob),
	})
}

// loginExportServer simulates Lose It: POST /account/login sets liauth=goodToken
// (when creds are present); GET /export/data returns the ZIP only when the
// request carries liauth==goodToken, else a tiny "expired" page. It counts logins.
func loginExportServer(t *testing.T) (*httptest.Server, *int) {
	t.Helper()
	logins := 0
	zipBytes := bigZip(t)
	mux := http.NewServeMux()
	mux.HandleFunc("/account/login", func(w http.ResponseWriter, r *http.Request) {
		logins++
		_ = r.ParseForm()
		if r.PostForm.Get("username") == "" || r.PostForm.Get("password") == "" ||
			r.PostForm.Get("grant_type") != "password" {
			w.WriteHeader(http.StatusNotFound)
			return
		}
		http.SetCookie(w, &http.Cookie{Name: "fn_auth", Value: goodToken})
		http.SetCookie(w, &http.Cookie{Name: loginCookie, Value: goodToken})
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte("{}"))
	})
	mux.HandleFunc("/export/data", func(w http.ResponseWriter, r *http.Request) {
		if c, err := r.Cookie(loginCookie); err == nil && c.Value == goodToken {
			_, _ = w.Write(zipBytes)
			return
		}
		_, _ = w.Write([]byte("<html>login</html>"))
	})
	srv := httptest.NewServer(mux)
	t.Cleanup(srv.Close)
	return srv, &logins
}

func testCfg(srv *httptest.Server, tokenPath string, withCreds bool) *config.Config {
	c := &config.Config{
		TokenPath: tokenPath,
		ExportURL: srv.URL + "/export/data",
		LoginURL:  srv.URL + "/account/login",
	}
	if withCreds {
		c.Email = "user@example.com"
		c.Password = "pw"
	}
	return c
}

func TestLoginReturnsLiauthCookie(t *testing.T) {
	srv, n := loginExportServer(t)
	cfg := testCfg(srv, filepath.Join(t.TempDir(), "token"), true)
	tok, err := Login(context.Background(), cfg)
	if err != nil {
		t.Fatal(err)
	}
	if tok != goodToken {
		t.Errorf("token = %q, want %q", tok, goodToken)
	}
	if *n != 1 {
		t.Errorf("logins = %d, want 1", *n)
	}
}

func TestLoginRequiresCredentials(t *testing.T) {
	srv, _ := loginExportServer(t)
	cfg := testCfg(srv, filepath.Join(t.TempDir(), "token"), false) // no email/password
	if _, err := Login(context.Background(), cfg); err == nil {
		t.Fatal("expected an error when credentials are missing")
	}
}

func TestSaveAndReadToken(t *testing.T) {
	t.Setenv(config.EnvToken, "") // force the file path, not the env token
	p := filepath.Join(t.TempDir(), "nested", "token")
	cfg := &config.Config{TokenPath: p}
	if err := SaveToken(cfg, goodToken); err != nil {
		t.Fatal(err)
	}
	if got := ReadToken(cfg); got != goodToken {
		t.Errorf("ReadToken = %q, want %q", got, goodToken)
	}
}

// TestSaveTokenWritesOwnerOnly pins the least-privilege guarantee: the liauth
// session token is a reusable credential, so its file must be owner-only (0600)
// and its created parent dir owner-only (0700). If someone loosens SaveToken (or
// swaps back to a wider mode), this fails. Permission bits are advisory on
// Windows — os.Stat synthesizes them — so assert them only where they are real.
func TestSaveTokenWritesOwnerOnly(t *testing.T) {
	t.Setenv(config.EnvToken, "")
	path := filepath.Join(t.TempDir(), "nested", "token")
	cfg := &config.Config{TokenPath: path}
	if err := SaveToken(cfg, goodToken); err != nil {
		t.Fatal(err)
	}
	if runtime.GOOS == "windows" {
		return
	}
	fi, err := os.Stat(path)
	if err != nil {
		t.Fatal(err)
	}
	if got := fi.Mode().Perm(); got != 0o600 {
		t.Errorf("token file mode = %#o, want 0600", got)
	}
	di, err := os.Stat(filepath.Dir(path))
	if err != nil {
		t.Fatal(err)
	}
	if got := di.Mode().Perm(); got != 0o700 {
		t.Errorf("token dir mode = %#o, want 0700", got)
	}
}

// TestSaveTokenReTightensExistingFile pins the re-tighten behavior: re-saving
// over a token file that already exists with loose permissions must restore 0600
// (os.WriteFile/O_CREATE alone would not). Removing the explicit Chmod fails this.
func TestSaveTokenReTightensExistingFile(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("file permission bits are advisory on Windows")
	}
	t.Setenv(config.EnvToken, "")
	path := filepath.Join(t.TempDir(), "token")
	if err := os.WriteFile(path, []byte("OLD\n"), 0o644); err != nil {
		t.Fatal(err)
	}
	cfg := &config.Config{TokenPath: path}
	if err := SaveToken(cfg, goodToken); err != nil {
		t.Fatal(err)
	}
	fi, err := os.Stat(path)
	if err != nil {
		t.Fatal(err)
	}
	if got := fi.Mode().Perm(); got != 0o600 {
		t.Errorf("token file mode after re-save = %#o, want 0600 (re-tighten)", got)
	}
}

func TestFetchZipAutoLoginWhenNoToken(t *testing.T) {
	t.Setenv(config.EnvToken, "")
	srv, n := loginExportServer(t)
	tokenPath := filepath.Join(t.TempDir(), "token")
	cfg := testCfg(srv, tokenPath, true)

	data, err := FetchZip(context.Background(), cfg)
	if err != nil {
		t.Fatal(err)
	}
	if !looksLikeZip(data) {
		t.Fatal("expected ZIP bytes")
	}
	if *n != 1 {
		t.Errorf("logins = %d, want 1", *n)
	}
	if got := ReadToken(cfg); got != goodToken {
		t.Errorf("token not persisted: %q", got)
	}
}

func TestFetchZipRefreshesExpiredToken(t *testing.T) {
	t.Setenv(config.EnvToken, "")
	srv, n := loginExportServer(t)
	tokenPath := filepath.Join(t.TempDir(), "token")
	cfg := testCfg(srv, tokenPath, true)
	if err := os.WriteFile(tokenPath, []byte("STALE\n"), 0o600); err != nil {
		t.Fatal(err)
	}

	data, err := FetchZip(context.Background(), cfg)
	if err != nil {
		t.Fatal(err)
	}
	if !looksLikeZip(data) {
		t.Fatal("expected ZIP after refresh")
	}
	if *n != 1 {
		t.Errorf("logins = %d, want 1 (refresh only)", *n)
	}
}

func TestFetchZipNoTokenNoCredentialsErrors(t *testing.T) {
	t.Setenv(config.EnvToken, "")
	srv, _ := loginExportServer(t)
	cfg := testCfg(srv, filepath.Join(t.TempDir(), "token"), false)
	_, err := FetchZip(context.Background(), cfg)
	if err == nil {
		t.Fatal("expected an error with no token and no credentials")
	}
	if !strings.Contains(strings.ToLower(err.Error()), "login") {
		t.Errorf("error should point at login: %v", err)
	}
}
