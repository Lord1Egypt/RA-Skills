// Package auth owns the OAuth2 loopback login flow and the on-disk token cache.
//
// The Python google-health-cli held no credentials — the external `ghealth`
// binary owned OAuth and token state. This self-contained Go port mints and
// refreshes its own token (GOAL.md §8, §22). The cache file holds the
// *oauth2.Token JSON and is written owner-only (0600) because it is a credential.
package auth

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"log/slog"
	"net/http"
	"os"
	"path/filepath"

	"golang.org/x/oauth2"
)

// LoadToken reads the cached *oauth2.Token. A missing file is not an error — it
// returns (nil, nil) so callers can prompt for `auth login`. A corrupt cache is
// likewise treated as "no token" so the next login overwrites it.
func LoadToken(path string) (*oauth2.Token, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		if errors.Is(err, os.ErrNotExist) {
			return nil, nil
		}
		return nil, fmt.Errorf("read token cache %s: %w", path, err)
	}
	var tok oauth2.Token
	if err := json.Unmarshal(data, &tok); err != nil {
		return nil, nil // corrupt → treat as absent.
	}
	if tok.AccessToken == "" && tok.RefreshToken == "" {
		return nil, nil
	}
	return &tok, nil
}

// SaveToken writes the token cache with owner-only (0600) permissions.
//
// It uses os.OpenFile with O_TRUNC rather than os.WriteFile because WriteFile
// will NOT re-restrict permissions on a file that already exists (GOAL.md §8):
// passing the mode to OpenFile applies it to a freshly created file, and we
// additionally Chmod to tighten an existing one. On Windows the Unix bits are
// largely advisory, so a Chmod failure there must not fail the command — it is
// ignored (best-effort), matching speediance-cli-go and the Python try/except.
func SaveToken(path string, tok *oauth2.Token) error {
	if dir := filepath.Dir(path); dir != "" && dir != "." {
		if err := os.MkdirAll(dir, 0o700); err != nil {
			return fmt.Errorf("create token cache dir %s: %w", dir, err)
		}
	}

	f, err := os.OpenFile(path, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0o600)
	if err != nil {
		return fmt.Errorf("open token cache %s: %w", path, err)
	}
	defer func() { _ = f.Close() }()
	_ = f.Chmod(0o600) // best-effort re-tighten; ignored on Windows.

	enc := json.NewEncoder(f)
	enc.SetIndent("", "  ")
	// G117: persisting the OAuth token (which holds the access/refresh secrets) to
	// disk is the entire purpose of the token cache; it is written owner-only
	// (0600) above, so marshaling its secret fields here is by design.
	if err := enc.Encode(tok); err != nil { //nolint:gosec // G117: token cache must marshal the secret token (0600).
		return fmt.Errorf("write token cache %s: %w", path, err)
	}
	return nil
}

// MigrateLegacyToken relocates a token from a previous default location to the
// current one, exactly once and conservatively (shared CLI conventions §7):
//   - no-op if either path is empty or they are identical;
//   - never clobbers a token already at newPath;
//   - no-op on a missing/corrupt/unreadable legacy file (nothing live to move);
//   - removes the legacy file only after the new copy is safely written.
//
// It is best-effort by intent: a failure just means the next login writes fresh,
// so callers should log and continue rather than abort.
func MigrateLegacyToken(newPath, legacyPath string) (migrated bool, err error) {
	if newPath == "" || legacyPath == "" || newPath == legacyPath {
		return false, nil
	}
	if _, err := os.Stat(newPath); err == nil {
		return false, nil // never overwrite a token already at the destination.
	}
	tok, lerr := LoadToken(legacyPath)
	if lerr != nil || tok == nil {
		return false, nil // missing/corrupt/unreadable legacy → nothing to relocate.
	}
	if err := SaveToken(newPath, tok); err != nil {
		return false, err
	}
	if err := os.Remove(legacyPath); err != nil && !errors.Is(err, os.ErrNotExist) {
		// The token is safely at newPath; only cleanup of the old copy failed.
		return true, fmt.Errorf("remove legacy token cache %s: %w", legacyPath, err)
	}
	return true, nil
}

// DeleteToken removes the token cache (used by `auth logout`). A missing file is
// not an error.
func DeleteToken(path string) error {
	if err := os.Remove(path); err != nil && !errors.Is(err, os.ErrNotExist) {
		return fmt.Errorf("delete token cache %s: %w", path, err)
	}
	return nil
}

// persistingSource wraps a refreshing TokenSource and re-saves the token to disk
// whenever .Token() yields a newer one (an access-token rotation after a
// refresh). x/oauth2 handles refresh-token rotation internally; we only need to
// persist the result so the on-disk access token stays fresh between runs
// (GOAL.md §8 — ghealth doesn't do this; we should).
type persistingSource struct {
	base   oauth2.TokenSource
	path   string
	last   *oauth2.Token
	logger *slog.Logger
}

func (p *persistingSource) Token() (*oauth2.Token, error) {
	tok, err := p.base.Token()
	if err != nil {
		return nil, err
	}
	if p.changed(tok) {
		if err := SaveToken(p.path, tok); err != nil {
			p.logger.Warn("could not persist refreshed token", "path", p.path, "err", err)
		}
		p.last = tok
	}
	return tok, nil
}

// changed reports whether tok differs from the last persisted token in a way
// worth writing (a new access token or a new expiry).
func (p *persistingSource) changed(tok *oauth2.Token) bool {
	if p.last == nil {
		return true
	}
	return tok.AccessToken != p.last.AccessToken || !tok.Expiry.Equal(p.last.Expiry)
}

// NewHTTPClient builds an *http.Client that injects the OAuth2 bearer token,
// auto-refreshes it, and persists any refreshed token back to disk. The base
// transport (timeout + optional retries) is supplied by the caller via ctx's
// oauth2.HTTPClient value; oauth2.NewClient layers the token transport on top
// and inherits the base client's Timeout (GOAL.md §4, §8).
func NewHTTPClient(ctx context.Context, cfg *oauth2.Config, tok *oauth2.Token, path string, logger *slog.Logger) *Client {
	if logger == nil {
		logger = slog.New(slog.NewTextHandler(os.Stderr, nil))
	}
	src := &persistingSource{
		base:   cfg.TokenSource(ctx, tok),
		path:   path,
		last:   tok, // seed so a valid cached token isn't needlessly rewritten.
		logger: logger,
	}
	return &Client{
		HTTP:   oauth2.NewClient(ctx, src),
		Source: src,
	}
}

// Client bundles the authenticated *http.Client with its TokenSource so callers
// can both make requests and force a token check (e.g. `doctor` confirms the
// token is usable without a full API call).
type Client struct {
	HTTP   *http.Client
	Source oauth2.TokenSource
}

// CurrentToken forces the TokenSource to produce a (possibly refreshed) token,
// surfacing any refresh error. Used by doctor to confirm the token is usable
// without making a full API call.
func (c *Client) CurrentToken() (*oauth2.Token, error) {
	return c.Source.Token()
}
