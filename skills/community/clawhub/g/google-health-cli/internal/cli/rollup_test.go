package cli

import (
	"encoding/json"
	"errors"
	"io"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

// rollupFixtureServer serves the committed steps rollup fixture for any request,
// recording each request body into *reqBody so a test can assert the outgoing
// civil range the window flags produced.
func rollupFixtureServer(t *testing.T) (srv *httptest.Server, reqBody *string) {
	t.Helper()
	body, err := os.ReadFile(filepath.Join("..", "..", "testdata", "fixtures", "steps_rollup.json"))
	if err != nil {
		t.Fatalf("read fixture: %v", err)
	}
	var captured string
	srv = httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		b, _ := io.ReadAll(r.Body)
		captured = string(b)
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write(body)
	}))
	t.Cleanup(srv.Close)
	return srv, &captured
}

func TestRollupDailyCommand(t *testing.T) {
	srv, reqBody := rollupFixtureServer(t)
	withBaseURL(t, srv.URL)
	cfg := testConfig(t, true)

	stdout, stderr, err := run(t, "--config", cfg, "rollup", "daily", "steps", "--date", "2026-06-16", "--days", "2")
	if err != nil {
		t.Fatalf("rollup daily: %v", err)
	}
	var arr []json.RawMessage
	if err := json.Unmarshal([]byte(stdout), &arr); err != nil {
		t.Fatalf("rollup stdout not a JSON array: %v\n%s", err, stdout)
	}
	if len(arr) != 2 {
		t.Errorf("got %d rollup rows, want 2", len(arr))
	}
	if !strings.Contains(stderr, "steps daily rollup(s)") {
		t.Errorf("stderr missing count hint: %q", stderr)
	}
	// --date 2026-06-16 --days 2 must roll up the civil window [2026-06-15,
	// 2026-06-17): pins that the rollup command feeds the window flags through
	// to the outgoing dailyRollUp range, not just that some request was made.
	if !strings.Contains(*reqBody, `"start":{"date":{"year":2026,"month":6,"day":15}}`) ||
		!strings.Contains(*reqBody, `"end":{"date":{"year":2026,"month":6,"day":17}}`) {
		t.Errorf("outgoing rollup range wrong for --date 2026-06-16 --days 2: %s", *reqBody)
	}
}

func TestRollupDailyGolden(t *testing.T) {
	srv, _ := rollupFixtureServer(t)
	withBaseURL(t, srv.URL)
	cfg := testConfig(t, true)

	stdout, _, err := run(t, "--config", cfg, "rollup", "daily", "steps", "--date", "2026-06-16", "--days", "2")
	if err != nil {
		t.Fatalf("rollup daily: %v", err)
	}
	assertGolden(t, "rollup_daily_steps.golden", []byte(stdout))
}

// TestRollupDailyUnsupportedTypeIsUsageError: a type without dailyRollUp (here
// exercise) is rejected with the usage exit code, mirroring data list's
// non-listable handling.
func TestRollupDailyUnsupportedTypeIsUsageError(t *testing.T) {
	cfg := testConfig(t, true)
	_, _, err := run(t, "--config", cfg, "rollup", "daily", "exercise")
	var exit *ExitError
	if !errors.As(err, &exit) || exit.Code != ExitUsage {
		t.Fatalf("err = %v, want ExitError code %d", err, ExitUsage)
	}
}

func TestRollupDailyUnknownTypeIsUsageError(t *testing.T) {
	cfg := testConfig(t, true)
	_, _, err := run(t, "--config", cfg, "rollup", "daily", "not-a-type")
	var exit *ExitError
	if !errors.As(err, &exit) || exit.Code != ExitUsage {
		t.Fatalf("err = %v, want ExitError code %d", err, ExitUsage)
	}
}
