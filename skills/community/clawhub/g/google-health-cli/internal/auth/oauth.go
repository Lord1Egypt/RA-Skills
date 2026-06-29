package auth

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"errors"
	"fmt"
	"log/slog"
	"net"
	"net/http"
	"os/exec"
	"runtime"
	"time"

	"golang.org/x/oauth2"
	"golang.org/x/oauth2/google"
)

// loginTimeout bounds the whole interactive flow: the user must finish the
// browser consent and the loopback callback must fire within this window
// (GOAL.md §8).
const loginTimeout = 5 * time.Minute

// OAuthConfig builds the oauth2.Config for the Google Health read scope. The
// RedirectURL is filled in by Login once the loopback port is known. Endpoint is
// google.Endpoint (accounts.google.com authorize + oauth2.googleapis.com token).
func OAuthConfig(clientID, clientSecret string, scopes []string) *oauth2.Config {
	return &oauth2.Config{
		ClientID:     clientID,
		ClientSecret: clientSecret,
		Scopes:       scopes,
		Endpoint:     google.Endpoint,
	}
}

// LoginResult is returned by Login: the minted token plus the auth URL that was
// opened (useful for logging / when the browser can't open automatically).
type LoginResult struct {
	Token   *oauth2.Token
	AuthURL string
}

// Login runs the loopback OAuth2 + PKCE flow (GOAL.md §8):
//
//   - bind a loopback listener on 127.0.0.1:<random port> and set RedirectURL;
//   - generate a PKCE verifier and a random state;
//   - build the consent URL with access_type=offline + prompt=consent so Google
//     always returns a refresh_token;
//   - open the browser, serve /callback, validate state, capture ?code=;
//   - exchange the code (with the PKCE verifier) for a token.
//
// openBrowser is injectable so tests can drive the flow without a real browser;
// when nil, the platform default is used. The returned token is NOT persisted —
// the caller writes it to the cache.
func Login(ctx context.Context, cfg *oauth2.Config, openBrowser func(string) error, logger *slog.Logger) (*LoginResult, error) {
	if logger == nil {
		logger = slog.Default()
	}
	if openBrowser == nil {
		openBrowser = OpenBrowser
	}

	ln, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		return nil, fmt.Errorf("start loopback listener: %w", err)
	}
	defer func() { _ = ln.Close() }()

	port := ln.Addr().(*net.TCPAddr).Port
	cfg.RedirectURL = fmt.Sprintf("http://127.0.0.1:%d/callback", port)

	verifier := oauth2.GenerateVerifier()
	state, err := randomState()
	if err != nil {
		return nil, err
	}
	authURL := cfg.AuthCodeURL(state,
		oauth2.AccessTypeOffline,
		oauth2.S256ChallengeOption(verifier),
		oauth2.SetAuthURLParam("prompt", "consent"))

	// The callback handler reports its outcome on these channels.
	type result struct {
		code string
		err  error
	}
	resultCh := make(chan result, 1)

	mux := http.NewServeMux()
	mux.HandleFunc("/callback", func(w http.ResponseWriter, r *http.Request) {
		q := r.URL.Query()
		if e := q.Get("error"); e != "" {
			writeBrowserPage(w, false, "Authorization was denied. You can close this tab.")
			resultCh <- result{err: fmt.Errorf("authorization denied: %s", e)}
			return
		}
		if q.Get("state") != state {
			writeBrowserPage(w, false, "State mismatch — possible CSRF. You can close this tab.")
			resultCh <- result{err: errors.New("state mismatch in OAuth callback")}
			return
		}
		code := q.Get("code")
		if code == "" {
			writeBrowserPage(w, false, "No authorization code returned. You can close this tab.")
			resultCh <- result{err: errors.New("no authorization code in OAuth callback")}
			return
		}
		writeBrowserPage(w, true, "Authorized. You can close this tab and return to the terminal.")
		resultCh <- result{code: code}
	})

	srv := &http.Server{Handler: mux, ReadHeaderTimeout: 10 * time.Second}
	go func() { _ = srv.Serve(ln) }()
	defer func() {
		shutCtx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
		defer cancel()
		_ = srv.Shutdown(shutCtx)
	}()

	if err := openBrowser(authURL); err != nil {
		// Not fatal: the user can paste the URL manually. Surface it to stderr.
		logger.Warn("could not open browser automatically", "err", err)
	}

	timeout := time.NewTimer(loginTimeout)
	defer timeout.Stop()

	select {
	case <-ctx.Done():
		return nil, ctx.Err()
	case <-timeout.C:
		return nil, fmt.Errorf("timed out after %s waiting for OAuth callback", loginTimeout)
	case res := <-resultCh:
		if res.err != nil {
			return nil, res.err
		}
		tok, err := cfg.Exchange(ctx, res.code, oauth2.VerifierOption(verifier))
		if err != nil {
			return nil, fmt.Errorf("exchange authorization code: %w", err)
		}
		return &LoginResult{Token: tok, AuthURL: authURL}, nil
	}
}

// randomState returns a 32-hex-char anti-CSRF state value.
func randomState() (string, error) {
	b := make([]byte, 16)
	if _, err := rand.Read(b); err != nil {
		return "", fmt.Errorf("generate state: %w", err)
	}
	return hex.EncodeToString(b), nil
}

// writeBrowserPage renders a minimal status page in the user's browser after the
// redirect. Kept tiny and dependency-free.
func writeBrowserPage(w http.ResponseWriter, ok bool, msg string) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	status := "Success"
	if !ok {
		status = "Error"
	}
	_, _ = fmt.Fprintf(w, "<!doctype html><html><head><meta charset=\"utf-8\">"+
		"<title>google-health-cli — %s</title></head>"+
		"<body style=\"font-family:system-ui,sans-serif;max-width:32rem;margin:4rem auto;text-align:center\">"+
		"<h1>%s</h1><p>%s</p></body></html>", status, status, msg)
}

// OpenBrowser opens url in the user's default browser. Best-effort: a non-nil
// error means the caller should print the URL for the user to open manually.
func OpenBrowser(url string) error {
	var name string
	var args []string
	switch runtime.GOOS {
	case "windows":
		// rundll32 avoids cmd.exe quoting pitfalls with the URL's & and ?.
		name, args = "rundll32", []string{"url.dll,FileProtocolHandler", url}
	case "darwin":
		name, args = "open", []string{url}
	default:
		name, args = "xdg-open", []string{url}
	}
	// G204: the executable name is a hardcoded per-OS constant and url is passed
	// as a separate argv element (exec.Command spawns no shell), so there is no
	// command-injection vector — the gosec finding is a false positive here.
	cmd := exec.Command(name, args...) //nolint:gosec // G204: const exe name, URL passed as argv, no shell.
	return cmd.Start()
}
