package export

import (
	"archive/zip"
	"bytes"
	"context"
	"errors"
	"io"
	"os"
	"path/filepath"
	"testing"

	"github.com/stozo04/loseit-cli/internal/config"
)

// makeZip builds an in-memory ZIP from name→content members.
func makeZip(t *testing.T, members map[string]string) []byte {
	t.Helper()
	var buf bytes.Buffer
	zw := zip.NewWriter(&buf)
	for name, content := range members {
		w, err := zw.Create(name)
		if err != nil {
			t.Fatal(err)
		}
		if _, err := io.WriteString(w, content); err != nil {
			t.Fatal(err)
		}
	}
	if err := zw.Close(); err != nil {
		t.Fatal(err)
	}
	return buf.Bytes()
}

func TestReadCSVStripsBOMAndKeysByHeader(t *testing.T) {
	// A leading UTF-8 BOM on the header (U+FEFF) must not leak into the first
	// column name — the real export is UTF-8-with-BOM (utf-8-sig).
	z := makeZip(t, map[string]string{
		FoodLogsCSV: "\ufeff" + "Date,Name,Calories\n2026-06-16,Greek Yogurt,120\n",
	})
	rows, err := ReadCSV(z, FoodLogsCSV)
	if err != nil {
		t.Fatal(err)
	}
	if len(rows) != 1 {
		t.Fatalf("got %d rows, want 1", len(rows))
	}
	if rows[0]["Date"] != "2026-06-16" {
		t.Errorf("Date = %q (BOM not stripped?)", rows[0]["Date"])
	}
	if rows[0]["Name"] != "Greek Yogurt" {
		t.Errorf("Name = %q", rows[0]["Name"])
	}
}

func TestReadCSVRaggedRowTolerated(t *testing.T) {
	z := makeZip(t, map[string]string{
		FoodLogsCSV: "a,b,c\n1,2\n",
	})
	rows, err := ReadCSV(z, FoodLogsCSV)
	if err != nil {
		t.Fatal(err)
	}
	if rows[0]["a"] != "1" || rows[0]["b"] != "2" || rows[0]["c"] != "" {
		t.Errorf("ragged row = %v, want c empty", rows[0])
	}
}

func TestReadCSVAbsentMemberIsEmpty(t *testing.T) {
	z := makeZip(t, map[string]string{FoodLogsCSV: "Date\n2026-06-16\n"})
	rows, err := ReadCSV(z, SummaryCSV)
	if err != nil {
		t.Fatal(err)
	}
	if len(rows) != 0 {
		t.Errorf("absent member returned %d rows, want 0", len(rows))
	}
}

func TestLoadZipBytesFromFile(t *testing.T) {
	z := makeZip(t, map[string]string{FoodLogsCSV: "Date\n2026-06-16\n"})
	path := filepath.Join(t.TempDir(), "export.zip")
	if err := os.WriteFile(path, z, 0o600); err != nil {
		t.Fatal(err)
	}
	got, err := LoadZipBytes(context.Background(), &config.Config{}, path)
	if err != nil {
		t.Fatalf("LoadZipBytes: %v", err)
	}
	if !bytes.Equal(got, z) {
		t.Error("LoadZipBytes returned different bytes than written")
	}
}

func TestLoadZipBytesRejectsNonZip(t *testing.T) {
	path := filepath.Join(t.TempDir(), "not.zip")
	if err := os.WriteFile(path, []byte("<html>login</html>"), 0o600); err != nil {
		t.Fatal(err)
	}
	_, err := LoadZipBytes(context.Background(), &config.Config{}, path)
	var e *Error
	if !errors.As(err, &e) {
		t.Fatalf("err = %v, want *export.Error for a non-ZIP file", err)
	}
}

func TestLoadZipBytesMissingFile(t *testing.T) {
	_, err := LoadZipBytes(context.Background(), &config.Config{}, filepath.Join(t.TempDir(), "nope.zip"))
	if err == nil {
		t.Fatal("expected an error for a missing --zip file")
	}
}

func TestReadTokenEnvWinsAndTrims(t *testing.T) {
	t.Setenv(config.EnvToken, "  liauth-cookie  ")
	if got := ReadToken(&config.Config{TokenPath: "/nonexistent"}); got != "liauth-cookie" {
		t.Errorf("ReadToken (env) = %q, want trimmed cookie", got)
	}
}

func TestReadTokenFallsBackToFile(t *testing.T) {
	t.Setenv(config.EnvToken, "") // empty env → fall through to the file.
	path := filepath.Join(t.TempDir(), "token")
	if err := os.WriteFile(path, []byte("file-cookie\n"), 0o600); err != nil {
		t.Fatal(err)
	}
	if got := ReadToken(&config.Config{TokenPath: path}); got != "file-cookie" {
		t.Errorf("ReadToken (file) = %q, want file-cookie", got)
	}
}

func TestReadTokenNoneIsEmpty(t *testing.T) {
	t.Setenv(config.EnvToken, "")
	if got := ReadToken(&config.Config{TokenPath: filepath.Join(t.TempDir(), "absent")}); got != "" {
		t.Errorf("ReadToken (none) = %q, want empty", got)
	}
}
