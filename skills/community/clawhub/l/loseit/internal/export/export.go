// Package export obtains the Lose It! data export and reads its CSVs.
//
// Two paths supply the export ZIP, mirroring the Python tool:
//
//   - --zip PATH: read a downloaded export, no token needed.
//   - cookie fetch: GET export_url with the liauth/fn_auth session cookies. When
//     the saved cookie is missing or expired and email/password are configured,
//     the cookie fetch logs in automatically (see login.go) and retries — so it
//     is self-sufficient like the other collectors.
//
// Export ZIP layout (confirmed from the real export):
//
//	food-logs.csv             Date,Name,Icon,Meal,Quantity,Units,Calories,Deleted,
//	                          Fat (g),Protein (g),Carbohydrates (g),Saturated Fat (g),
//	                          Sugars (g),Fiber (g),Cholesterol (mg),Sodium (mg)
//	daily-calorie-summary.csv Date,Food cals,Exercise cals,Budget cals,EER
package export

import (
	"archive/zip"
	"bufio"
	"bytes"
	"context"
	"encoding/csv"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/stozo04/loseit-cli/internal/config"
)

// Names of the CSV members inside the export ZIP.
const (
	FoodLogsCSV = "food-logs.csv"
	SummaryCSV  = "daily-calorie-summary.csv"
)

const userAgent = "loseit-cli"

// Error is a typed domain error for export/parse failures. The CLI maps any
// error from the export path to exit code 2; this type carries the user-facing
// message.
type Error struct{ msg string }

func (e *Error) Error() string { return e.msg }

func newErr(format string, a ...any) *Error {
	return &Error{msg: fmt.Sprintf(format, a...)}
}

// ReadToken returns the liauth session cookie value, or "" if none is available.
// The LOSEIT_TOKEN environment variable wins; otherwise the token_path file is
// read (its ~ is expanded). A missing or unreadable file yields "".
func ReadToken(cfg *config.Config) string {
	if v, ok := os.LookupEnv(config.EnvToken); ok && v != "" {
		return strings.TrimSpace(v)
	}
	data, err := os.ReadFile(expandUser(cfg.TokenPath))
	if err != nil {
		return ""
	}
	return strings.TrimSpace(string(data))
}

// HasToken reports whether a token is available without exposing its value.
func HasToken(cfg *config.Config) bool { return ReadToken(cfg) != "" }

// LoadZipBytes returns the export ZIP bytes. When zipPath is set it reads that
// downloaded file (no token); otherwise it fetches via the session cookie.
func LoadZipBytes(ctx context.Context, cfg *config.Config, zipPath string) ([]byte, error) {
	if zipPath != "" {
		data, err := os.ReadFile(expandUser(zipPath))
		if err != nil {
			return nil, newErr("reading %s: %v", zipPath, err)
		}
		if !looksLikeZip(data) {
			return nil, newErr("%s is not a ZIP file.", zipPath)
		}
		return data, nil
	}
	return FetchZip(ctx, cfg)
}

// errExpired signals that the export response wasn't a valid ZIP — typically an
// expired liauth cookie (Lose It serves an HTML login page). Auto-login can
// recover from it, so FetchZip treats it as retryable rather than terminal.
var errExpired = errors.New("export response was not a ZIP (token likely expired)")

// FetchZip downloads the export ZIP using the liauth session cookie. It is
// self-sufficient when email/password are configured: if no cookie is saved it
// logs in first, and if a saved cookie is expired it logs in again and retries
// once. With only a manually-saved cookie (no credentials) it still works until
// that cookie expires.
func FetchZip(ctx context.Context, cfg *config.Config) ([]byte, error) {
	token := ReadToken(cfg)

	// No saved cookie: log in if we can, otherwise explain the options.
	if token == "" {
		if !cfg.HasCredentials() {
			return nil, newErr(
				"No Lose It token or credentials. Run `loseit-cli login` (needs %s/%s or "+
					"email/password in config.json), or pass --zip PATH to parse a downloaded export.",
				config.EnvEmail, config.EnvPassword,
			)
		}
		t, err := loginAndSave(ctx, cfg)
		if err != nil {
			return nil, err
		}
		token = t
	}

	data, err := fetchWithToken(ctx, cfg, token)
	if err == nil {
		return data, nil
	}
	if !errors.Is(err, errExpired) {
		return nil, err // hard transport/read error — not recoverable by login.
	}

	// Saved cookie was expired. Refresh via login (if we have creds) and retry once.
	if !cfg.HasCredentials() {
		return nil, newErr(
			"The saved liauth token is expired and no credentials are set to refresh it. "+
				"Run `loseit-cli login` with %s/%s (or config email/password), or use --zip PATH.",
			config.EnvEmail, config.EnvPassword,
		)
	}
	t, lerr := loginAndSave(ctx, cfg)
	if lerr != nil {
		return nil, lerr
	}
	data, err = fetchWithToken(ctx, cfg, t)
	if err != nil {
		if errors.Is(err, errExpired) {
			return nil, newErr("logged in, but the export still wasn't a ZIP — Lose It may have changed its export endpoint.")
		}
		return nil, err
	}
	return data, nil
}

// fetchWithToken performs the export GET with the given liauth cookie, returning
// the ZIP bytes or errExpired when the response isn't a valid ZIP.
func fetchWithToken(ctx context.Context, cfg *config.Config, token string) ([]byte, error) {
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, cfg.ExportURL, nil)
	if err != nil {
		return nil, newErr("building export request: %v", err)
	}
	// liauth and fn_auth carry the same session value; send both.
	req.Header.Set("Cookie", fmt.Sprintf("liauth=%s; fn_auth=%s", token, token))
	req.Header.Set("User-Agent", userAgent)

	client := &http.Client{Timeout: 120 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return nil, newErr("export request failed: %v", err)
	}
	defer func() { _ = resp.Body.Close() }()

	data, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, newErr("reading export response failed: %v", err)
	}
	// A valid export is a non-trivial ZIP. An HTML login page (expired cookie)
	// fails both checks.
	if len(data) <= 1000 || !looksLikeZip(data) {
		return nil, errExpired
	}
	return data, nil
}

// ReadCSV returns header-keyed rows for the named member inside the ZIP, like
// Python's csv.DictReader. A member that is absent yields an empty slice (nil),
// matching the Python tool. The stream is UTF-8 BOM-stripped (utf-8-sig).
func ReadCSV(zipBytes []byte, name string) ([]map[string]string, error) {
	zr, err := zip.NewReader(bytes.NewReader(zipBytes), int64(len(zipBytes)))
	if err != nil {
		return nil, newErr("opening export ZIP: %v", err)
	}
	for _, f := range zr.File {
		if f.Name == name {
			return readZipCSV(f)
		}
	}
	return nil, nil
}

func readZipCSV(f *zip.File) ([]map[string]string, error) {
	rc, err := f.Open()
	if err != nil {
		return nil, newErr("opening %s: %v", f.Name, err)
	}
	defer func() { _ = rc.Close() }()
	return parseCSV(rc)
}

// parseCSV reads CSV into header-keyed rows. Ragged rows are tolerated: missing
// trailing columns become "" (csv.DictReader yields None; our numeric/string
// parse treats both as empty), extra columns are dropped.
func parseCSV(r io.Reader) ([]map[string]string, error) {
	br := bufio.NewReader(r)
	if b, err := br.Peek(3); err == nil && bytes.Equal(b, []byte{0xEF, 0xBB, 0xBF}) {
		_, _ = br.Discard(3)
	}

	cr := csv.NewReader(br)
	cr.FieldsPerRecord = -1 // tolerate ragged rows like csv.DictReader.
	cr.LazyQuotes = true

	records, err := cr.ReadAll()
	if err != nil {
		return nil, newErr("parsing CSV: %v", err)
	}
	if len(records) == 0 {
		return nil, nil
	}

	header := records[0]
	rows := make([]map[string]string, 0, len(records)-1)
	for _, rec := range records[1:] {
		m := make(map[string]string, len(header))
		for i, h := range header {
			if i < len(rec) {
				m[h] = rec[i]
			} else {
				m[h] = ""
			}
		}
		rows = append(rows, m)
	}
	return rows, nil
}

// looksLikeZip reports whether data begins with the ZIP local-file signature.
func looksLikeZip(data []byte) bool {
	return len(data) >= 2 && data[0] == 'P' && data[1] == 'K'
}

// expandUser expands a leading ~ to the user's home directory, like Python's
// os.path.expanduser. A bare ~ or ~/… (or ~\… on Windows) is expanded; anything
// else is returned unchanged.
func expandUser(p string) string {
	if p == "~" || strings.HasPrefix(p, "~/") || strings.HasPrefix(p, `~\`) {
		home, err := os.UserHomeDir()
		if err != nil {
			return p
		}
		if p == "~" {
			return home
		}
		return filepath.Join(home, p[2:])
	}
	return p
}
