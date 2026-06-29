package auth

import (
	"errors"
	"log/slog"
	"os"
	"path/filepath"
	"runtime"
	"testing"
	"time"

	"golang.org/x/oauth2"
)

func TestSaveLoadRoundTrip(t *testing.T) {
	path := filepath.Join(t.TempDir(), "sub", "token.json")
	want := &oauth2.Token{
		AccessToken:  "access-123",
		TokenType:    "Bearer",
		RefreshToken: "refresh-456",
		Expiry:       time.Date(2026, 6, 17, 12, 0, 0, 0, time.UTC),
	}
	if err := SaveToken(path, want); err != nil {
		t.Fatalf("SaveToken: %v", err)
	}
	got, err := LoadToken(path)
	if err != nil {
		t.Fatalf("LoadToken: %v", err)
	}
	if got == nil {
		t.Fatal("LoadToken returned nil for a saved token")
	}
	if got.AccessToken != want.AccessToken || got.RefreshToken != want.RefreshToken || got.TokenType != want.TokenType {
		t.Errorf("round trip mismatch: %+v", got)
	}
	if !got.Expiry.Equal(want.Expiry) {
		t.Errorf("Expiry = %v, want %v", got.Expiry, want.Expiry)
	}
}

func TestSaveTokenPerms(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("Unix permission bits are advisory on Windows")
	}
	path := filepath.Join(t.TempDir(), "token.json")
	if err := SaveToken(path, &oauth2.Token{AccessToken: "x"}); err != nil {
		t.Fatalf("SaveToken: %v", err)
	}
	info, err := os.Stat(path)
	if err != nil {
		t.Fatalf("stat: %v", err)
	}
	if perm := info.Mode().Perm(); perm != 0o600 {
		t.Errorf("perm = %o, want 600", perm)
	}
}

func TestLoadMissingIsNil(t *testing.T) {
	got, err := LoadToken(filepath.Join(t.TempDir(), "does-not-exist.json"))
	if err != nil {
		t.Fatalf("LoadToken(missing) error = %v, want nil", err)
	}
	if got != nil {
		t.Errorf("LoadToken(missing) = %+v, want nil", got)
	}
}

func TestLoadCorruptIsNil(t *testing.T) {
	path := filepath.Join(t.TempDir(), "token.json")
	if err := os.WriteFile(path, []byte("{not json"), 0o600); err != nil {
		t.Fatal(err)
	}
	got, err := LoadToken(path)
	if err != nil {
		t.Fatalf("LoadToken(corrupt) error = %v, want nil (treat as absent)", err)
	}
	if got != nil {
		t.Errorf("LoadToken(corrupt) = %+v, want nil", got)
	}
}

func TestDeleteToken(t *testing.T) {
	path := filepath.Join(t.TempDir(), "token.json")
	if err := SaveToken(path, &oauth2.Token{AccessToken: "x"}); err != nil {
		t.Fatal(err)
	}
	if err := DeleteToken(path); err != nil {
		t.Fatalf("DeleteToken: %v", err)
	}
	if _, err := os.Stat(path); !os.IsNotExist(err) {
		t.Errorf("token still present after delete: %v", err)
	}
	// Deleting an already-absent file is not an error.
	if err := DeleteToken(path); err != nil {
		t.Errorf("DeleteToken(missing) = %v, want nil", err)
	}
}

func TestMigrateLegacyToken(t *testing.T) {
	dir := t.TempDir()
	legacy := filepath.Join(dir, "roaming", "token.json")
	newPath := filepath.Join(dir, "local", "token.json")
	if err := SaveToken(legacy, &oauth2.Token{AccessToken: "a", RefreshToken: "r", TokenType: "Bearer"}); err != nil {
		t.Fatal(err)
	}

	moved, err := MigrateLegacyToken(newPath, legacy)
	if err != nil || !moved {
		t.Fatalf("MigrateLegacyToken: moved=%v err=%v, want true/nil", moved, err)
	}
	if _, serr := os.Stat(legacy); !errors.Is(serr, os.ErrNotExist) {
		t.Error("legacy token still present after migration")
	}
	got, err := LoadToken(newPath)
	if err != nil || got == nil || got.AccessToken != "a" {
		t.Fatalf("relocated token missing/wrong: %+v err=%v", got, err)
	}

	// Idempotent: a second run is a no-op (legacy is gone).
	if moved2, _ := MigrateLegacyToken(newPath, legacy); moved2 {
		t.Error("second migration reported a move, want no-op")
	}
}

func TestMigrateLegacyTokenNeverClobbers(t *testing.T) {
	dir := t.TempDir()
	legacy := filepath.Join(dir, "roaming", "token.json")
	newPath := filepath.Join(dir, "local", "token.json")
	if err := SaveToken(legacy, &oauth2.Token{AccessToken: "old"}); err != nil {
		t.Fatal(err)
	}
	if err := SaveToken(newPath, &oauth2.Token{AccessToken: "current"}); err != nil {
		t.Fatal(err)
	}

	moved, err := MigrateLegacyToken(newPath, legacy)
	if err != nil || moved {
		t.Fatalf("MigrateLegacyToken: moved=%v err=%v, want false/nil (destination occupied)", moved, err)
	}
	got, _ := LoadToken(newPath)
	if got == nil || got.AccessToken != "current" {
		t.Errorf("destination token was clobbered: %+v", got)
	}
	if _, serr := os.Stat(legacy); errors.Is(serr, os.ErrNotExist) {
		t.Error("legacy token was removed despite no migration")
	}
}

func TestMigrateLegacyTokenNoLegacy(t *testing.T) {
	dir := t.TempDir()
	moved, err := MigrateLegacyToken(filepath.Join(dir, "new.json"), filepath.Join(dir, "absent.json"))
	if err != nil || moved {
		t.Fatalf("MigrateLegacyToken(no legacy): moved=%v err=%v, want false/nil", moved, err)
	}
}

// staticSource returns a fixed token, simulating a refresh that produced it.
type staticSource struct{ tok *oauth2.Token }

func (s staticSource) Token() (*oauth2.Token, error) { return s.tok, nil }

func TestPersistingSourceWritesOnChange(t *testing.T) {
	path := filepath.Join(t.TempDir(), "token.json")
	old := &oauth2.Token{AccessToken: "old", Expiry: time.Date(2026, 6, 17, 12, 0, 0, 0, time.UTC)}
	refreshed := &oauth2.Token{AccessToken: "new", Expiry: time.Date(2026, 6, 17, 13, 0, 0, 0, time.UTC)}

	ps := &persistingSource{
		base:   staticSource{refreshed},
		path:   path,
		last:   old,
		logger: slog.New(slog.NewTextHandler(os.Stderr, nil)),
	}
	tok, err := ps.Token()
	if err != nil {
		t.Fatalf("Token: %v", err)
	}
	if tok.AccessToken != "new" {
		t.Errorf("Token().AccessToken = %q, want new", tok.AccessToken)
	}
	saved, err := LoadToken(path)
	if err != nil || saved == nil {
		t.Fatalf("expected persisted token, got %+v err=%v", saved, err)
	}
	if saved.AccessToken != "new" {
		t.Errorf("persisted AccessToken = %q, want new", saved.AccessToken)
	}
}

func TestPersistingSourceSkipsWhenUnchanged(t *testing.T) {
	path := filepath.Join(t.TempDir(), "token.json")
	same := &oauth2.Token{AccessToken: "same", Expiry: time.Date(2026, 6, 17, 12, 0, 0, 0, time.UTC)}

	ps := &persistingSource{
		base:   staticSource{same},
		path:   path,
		last:   same,
		logger: slog.New(slog.NewTextHandler(os.Stderr, nil)),
	}
	if _, err := ps.Token(); err != nil {
		t.Fatalf("Token: %v", err)
	}
	// Unchanged token must not write the cache.
	if _, err := os.Stat(path); !os.IsNotExist(err) {
		t.Errorf("cache written despite no change: %v", err)
	}
}
