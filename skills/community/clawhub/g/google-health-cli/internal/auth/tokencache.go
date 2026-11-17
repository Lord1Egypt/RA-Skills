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
	"io"
	"log/slog"
	"net/http"
	"os"
	"path/filepath"

	"golang.org/x/oauth2"
)

// ErrNotTokenCache means the configured token cache path holds a file that is
// not an OAuth token, so writing or deleting it could destroy unrelated data.
var ErrNotTokenCache = errors.New("token cache path holds a file this tool did not write")

const (
	cacheOwner            = "google-health-cli"
	conventionalCacheDir  = "google-health-cli"
	conventionalCacheName = "token.json"
	maxTokenCacheBytes    = 64 << 10
)

type ownedToken struct {
	*oauth2.Token
	Owner string `json:"owner"`
}

func ensureTokenCacheIsOurs(path, provenRefreshToken string) error {
	data, err := readTokenCacheFile(path)
	if errors.Is(err, os.ErrNotExist) {
		return nil
	}
	if err != nil {
		return err
	}
	if isOurTokenCache(path, data, provenRefreshToken) {
		return nil
	}
	return refuseTokenCache(path)
}

func readTokenCacheFile(path string) ([]byte, error) {
	info, err := os.Lstat(path)
	if err != nil {
		if errors.Is(err, os.ErrNotExist) {
			return nil, err
		}
		return nil, fmt.Errorf("stat token cache %s: %w", path, err)
	}
	if !info.Mode().IsRegular() || info.Size() > maxTokenCacheBytes {
		return nil, refuseTokenCache(path)
	}
	f, err := os.Open(path)
	if err != nil {
		return nil, fmt.Errorf("read token cache %s: %w", path, err)
	}
	defer func() { _ = f.Close() }()
	opened, err := f.Stat()
	if err != nil {
		return nil, fmt.Errorf("stat token cache %s: %w", path, err)
	}
	if !opened.Mode().IsRegular() || !os.SameFile(info, opened) {
		return nil, refuseTokenCache(path)
	}
	data, err := io.ReadAll(io.LimitReader(f, maxTokenCacheBytes+1))
	if err != nil {
		return nil, fmt.Errorf("read token cache %s: %w", path, err)
	}
	if len(data) > maxTokenCacheBytes {
		return nil, refuseTokenCache(path)
	}
	return data, nil
}

func isOurTokenCache(path string, data []byte, provenRefreshToken string) bool {
	if len(data) > maxTokenCacheBytes {
		return false
	}
	cached := ownedToken{Token: &oauth2.Token{}}
	if json.Unmarshal(data, &cached) != nil {
		return false
	}
	if cached.Owner == cacheOwner {
		return true
	}
	if provenRefreshToken != "" && cached.RefreshToken == provenRefreshToken {
		return true
	}
	holdsToken := cached.AccessToken != "" || cached.RefreshToken != ""
	return holdsToken && isConventionalCachePath(path)
}

func isConventionalCachePath(path string) bool {
	return filepath.Base(path) == conventionalCacheName &&
		filepath.Base(filepath.Dir(path)) == conventionalCacheDir
}

func refuseTokenCache(path string) error {
	return fmt.Errorf("%w: %s; point token_cache at a new path, or delete the file yourself if it is this tool's stale cache", ErrNotTokenCache, path)
}

// CheckTokenCacheWritable reports ErrNotTokenCache when SaveToken would refuse
// path, so a caller can fail before an interactive login rather than after it.
func CheckTokenCacheWritable(path string) error {
	return ensureTokenCacheIsOurs(path, "")
}

// LoadToken reads the cached *oauth2.Token. A missing file is not an error — it
// returns (nil, nil) so callers can prompt for `auth login`. A corrupt cache is
// likewise treated as "no token"; SaveToken and DeleteToken refuse to touch it
// (ErrNotTokenCache), so the user removes it before logging in again. A symlink,
// a non-regular file (device, FIFO, directory) or a file over 64 KiB is never
// read: LoadToken returns ErrNotTokenCache, because token_cache may come from an
// untrusted config.json and must not be able to hang or exhaust the process.
func LoadToken(path string) (*oauth2.Token, error) {
	data, err := readTokenCacheFile(path)
	if err != nil {
		if errors.Is(err, os.ErrNotExist) {
			return nil, nil
		}
		return nil, err
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

// SaveToken writes the token cache with owner-only (0600) permissions, through a
// temp file renamed over path, so the write is atomic and never follows a
// symlink swapped in after the ownership check. It refuses to replace an
// existing file this tool did not write (ErrNotTokenCache), so a misdirected
// token_cache can't clobber unrelated data.
func SaveToken(path string, tok *oauth2.Token) error {
	return saveToken(path, tok, "")
}

func saveToken(path string, tok *oauth2.Token, provenRefreshToken string) error {
	if err := ensureTokenCacheIsOurs(path, provenRefreshToken); err != nil {
		return err
	}
	dir := filepath.Dir(path)
	if err := os.MkdirAll(dir, 0o700); err != nil {
		return fmt.Errorf("create token cache dir %s: %w", dir, err)
	}

	tmp, err := os.CreateTemp(dir, ".token-*.tmp")
	if err != nil {
		return fmt.Errorf("create token cache %s: %w", path, err)
	}
	tmpPath := tmp.Name()
	committed := false
	defer func() {
		if !committed {
			_ = tmp.Close()
			_ = os.Remove(tmpPath)
		}
	}()
	_ = tmp.Chmod(0o600) // best-effort; CreateTemp already uses 0600, and Windows ignores the bits.

	enc := json.NewEncoder(tmp)
	enc.SetIndent("", "  ")
	// G117: persisting the OAuth token (which holds the access/refresh secrets) to
	// disk is the entire purpose of the token cache; it is written owner-only
	// (0600), so marshaling its secret fields here is by design.
	if err := enc.Encode(ownedToken{Token: tok, Owner: cacheOwner}); err != nil { //nolint:gosec // G117: token cache must marshal the secret token (0600).
		return fmt.Errorf("write token cache %s: %w", path, err)
	}
	if err := tmp.Close(); err != nil {
		return fmt.Errorf("write token cache %s: %w", path, err)
	}
	if err := os.Rename(tmpPath, path); err != nil {
		return fmt.Errorf("replace token cache %s: %w", path, err)
	}
	committed = true
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
// not an error; a file that is not an OAuth token is refused (ErrNotTokenCache).
func DeleteToken(path string) error {
	if err := ensureTokenCacheIsOurs(path, ""); err != nil {
		return err
	}
	if err := os.Remove(path); err != nil && !errors.Is(err, os.ErrNotExist) {
		return fmt.Errorf("delete token cache %s: %w", path, err)
	}
	return nil
}

// persistingSource wraps a refreshing TokenSource and re-saves the token to disk
// whenever .Token() yields a newer one (an access-token rotation after a
// refresh). x/oauth2 handles refresh-token rotation internally; we only need to
// persist the result so the on-disk OAuth token stays fresh between runs
// (GOAL.md §8 — ghealth doesn't do this; we should).
type persistingSource struct {
	base               oauth2.TokenSource
	path               string
	last               *oauth2.Token
	loadedRefreshToken string
	logger             *slog.Logger
}

func (p *persistingSource) Token() (*oauth2.Token, error) {
	tok, err := p.base.Token()
	if err != nil {
		return nil, err
	}
	if p.changed(tok) {
		if err := saveToken(p.path, tok, p.loadedRefreshToken); err != nil {
			p.logger.Warn("could not persist refreshed token", "path", p.path, "err", err)
		}
		p.last = tok
	}
	return tok, nil
}

// changed reports whether tok differs from the last persisted token in a way
// worth writing (a new bearer value or a new expiry).
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
	if tok != nil {
		src.loadedRefreshToken = tok.RefreshToken
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
