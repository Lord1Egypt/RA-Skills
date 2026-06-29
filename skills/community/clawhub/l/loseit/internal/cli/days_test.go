package cli

import (
	"archive/zip"
	"bytes"
	"encoding/json"
	"errors"
	"io"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

// The synthetic export mirrors tests/test_offline.py exactly: the confirmed
// food-logs.csv columns and rows (including a deleted 999-cal row that must be
// excluded) plus the daily-calorie-summary.csv.
const (
	foodHeader = "Date,Name,Icon,Meal,Quantity,Units,Calories,Deleted," +
		"Fat (g),Protein (g),Carbohydrates (g),Saturated Fat (g)," +
		"Sugars (g),Fiber (g),Cholesterol (mg),Sodium (mg)"

	foodCSV = foodHeader + "\n" +
		"2026-06-16,Greek Yogurt,icon,Breakfast,1,cup,120,false,0,22,9,0,9,0,10,80\n" +
		"2026-06-16,Banana,icon,Breakfast,1,each,105,false,0,1,27,0,14,3,0,1\n" +
		"2026-06-16,Chicken Breast,icon,Lunch,6,oz,280,false,6,52,0,2,0,0,120,150\n" +
		"2026-06-16,Old Deleted Food,icon,Lunch,1,each,999,true,50,0,50,0,0,0,0,0\n" +
		"2026-06-15,Protein Shake,icon,Snacks,1,scoop,120,false,1,24,3,0,2,1,5,90\n"

	summaryCSV = "Date,Food cals,Exercise cals,Budget cals,EER\n" +
		"2026-06-16,505,120,1663,2450\n" +
		"2026-06-15,120,0,1663,2450\n"
)

func makeExportZip(t *testing.T) []byte {
	t.Helper()
	var buf bytes.Buffer
	zw := zip.NewWriter(&buf)
	add := func(name, content string) {
		w, err := zw.Create(name)
		if err != nil {
			t.Fatal(err)
		}
		if _, err := io.WriteString(w, content); err != nil {
			t.Fatal(err)
		}
	}
	add("food-logs.csv", foodCSV)
	add("daily-calorie-summary.csv", summaryCSV)
	if err := zw.Close(); err != nil {
		t.Fatal(err)
	}
	return buf.Bytes()
}

func writeExportZip(t *testing.T) string {
	t.Helper()
	path := filepath.Join(t.TempDir(), "export.zip")
	if err := os.WriteFile(path, makeExportZip(t), 0o600); err != nil {
		t.Fatal(err)
	}
	return path
}

func TestDaysJSONGolden(t *testing.T) {
	zipPath := writeExportZip(t)
	stdout, _, err := run(t, "days", "--zip", zipPath, "--json", "--date", "2026-06-16", "--days", "7")
	if err != nil {
		t.Fatalf("days --json: %v", err)
	}
	assertGolden(t, "days_json.golden", []byte(stdout))
}

func TestDaysJSONValues(t *testing.T) {
	zipPath := writeExportZip(t)
	stdout, _, err := run(t, "days", "--zip", zipPath, "--json", "--date", "2026-06-16", "--days", "7")
	if err != nil {
		t.Fatalf("days --json: %v", err)
	}
	var got map[string]map[string]any
	if err := json.Unmarshal([]byte(stdout), &got); err != nil {
		t.Fatalf("days --json invalid: %v\n%s", err, stdout)
	}
	d := got["2026-06-16"]
	if d == nil {
		t.Fatal("missing 2026-06-16")
	}
	// JSON numbers decode to float64.
	checks := map[string]float64{
		"calories_food":       505,
		"protein_g":           75,
		"carbs_g":             36,
		"fat_g":               6,
		"fiber_g":             3,
		"loseit_budget":       1663,
		"loseit_under":        1158,
		"exercise_adjustment": 120,
	}
	for k, want := range checks {
		if v, ok := d[k].(float64); !ok || v != want {
			t.Errorf("2026-06-16 %s = %v, want %v", k, d[k], want)
		}
	}
	if d["source"] != "Lose It export" {
		t.Errorf("source = %v", d["source"])
	}
	if _, ok := got["2026-06-15"]; !ok {
		t.Error("expected 2026-06-15 in the 7-day window")
	}
}

func TestDaysJSONEmptyIsObject(t *testing.T) {
	zipPath := writeExportZip(t)
	// A window with no logged days must emit {} (not null, not []).
	stdout, _, err := run(t, "days", "--zip", zipPath, "--json", "--date", "2020-01-01", "--days", "1")
	if err != nil {
		t.Fatalf("days --json: %v", err)
	}
	if strings.TrimSpace(stdout) != "{}" {
		t.Errorf("empty result = %q, want {}", strings.TrimSpace(stdout))
	}
}

func TestDaysHumanTable(t *testing.T) {
	zipPath := writeExportZip(t)
	stdout, _, err := run(t, "days", "--zip", zipPath, "--date", "2026-06-16", "--days", "7")
	if err != nil {
		t.Fatalf("days: %v", err)
	}
	if !strings.Contains(stdout, "2026-06-16") || !strings.Contains(stdout, "505 cal") {
		t.Errorf("human table missing expected content:\n%s", stdout)
	}
}

func TestDaysBadDateExits64(t *testing.T) {
	zipPath := writeExportZip(t)
	_, _, err := run(t, "days", "--zip", zipPath, "--date", "not-a-date")
	var exit *ExitError
	if !errors.As(err, &exit) || exit.Code != ExitUsage {
		t.Fatalf("err = %v, want ExitError code %d", err, ExitUsage)
	}
}

func TestDaysMissingZipExits2(t *testing.T) {
	_, _, err := run(t, "days", "--zip", filepath.Join(t.TempDir(), "nope.zip"))
	var exit *ExitError
	if !errors.As(err, &exit) || exit.Code != ExitExport {
		t.Fatalf("err = %v, want ExitError code %d", err, ExitExport)
	}
}
