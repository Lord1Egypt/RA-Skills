package api

import (
	"context"
	"encoding/json"
	"errors"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

// stepsRollupResponse is a representative dataPoints:dailyRollUp envelope: two
// civil-day windows, newest first, each carrying the reconciled steps countSum.
// The empty "time" objects mirror what the live API returns for day-aligned
// bounds.
const stepsRollupResponse = `{"rollupDataPoints":[` +
	`{"civilStartTime":{"date":{"year":2026,"month":6,"day":16},"time":{}},"civilEndTime":{"date":{"year":2026,"month":6,"day":17},"time":{}},"steps":{"countSum":"8000"}},` +
	`{"civilStartTime":{"date":{"year":2026,"month":6,"day":15},"time":{}},"civilEndTime":{"date":{"year":2026,"month":6,"day":16},"time":{}},"steps":{"countSum":"10000"}}` +
	`]}`

func TestRollUpDaily_RequestAndDecode(t *testing.T) {
	var gotMethod, gotPath, gotBody string
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		gotMethod, gotPath = r.Method, r.URL.Path
		b, _ := io.ReadAll(r.Body)
		gotBody = string(b)
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(stepsRollupResponse))
	}))
	defer srv.Close()

	c := New(srv.Client(), srv.URL, "users/me", nil)
	steps, _ := LookupDataType("steps")
	from := time.Date(2026, 6, 15, 0, 0, 0, 0, time.UTC)
	to := time.Date(2026, 6, 17, 0, 0, 0, 0, time.UTC)

	pts, err := c.RollUpDaily(context.Background(), steps, from, to)
	if err != nil {
		t.Fatalf("RollUpDaily: %v", err)
	}

	if gotMethod != http.MethodPost {
		t.Errorf("method = %q, want POST", gotMethod)
	}
	wantPath := "/v4/users/me/dataTypes/steps/dataPoints:dailyRollUp"
	if gotPath != wantPath {
		t.Errorf("path = %q, want %q", gotPath, wantPath)
	}

	// The body must carry the civil [start, end) range and windowSizeDays:1, and
	// must NOT set pageSize — pageSize couples to the per-type duration cap and a
	// large value is rejected with INVALID_ROLLUP_QUERY_DURATION.
	var req map[string]any
	if err := json.Unmarshal([]byte(gotBody), &req); err != nil {
		t.Fatalf("request body not JSON: %v\n%s", err, gotBody)
	}
	if _, hasPageSize := req["pageSize"]; hasPageSize {
		t.Errorf("request must not set pageSize (couples to the duration cap): %s", gotBody)
	}
	if req["windowSizeDays"] != float64(1) {
		t.Errorf("windowSizeDays = %v, want 1", req["windowSizeDays"])
	}
	if !strings.Contains(gotBody, `"start":{"date":{"year":2026,"month":6,"day":15}}`) ||
		!strings.Contains(gotBody, `"end":{"date":{"year":2026,"month":6,"day":17}}`) {
		t.Errorf("civil range bounds wrong: %s", gotBody)
	}

	if len(pts) != 2 {
		t.Fatalf("got %d rollup rows, want 2", len(pts))
	}
	// Raw bytes are returned verbatim (dumb collector).
	if !strings.Contains(string(pts[0]), `"countSum":"8000"`) {
		t.Errorf("row 0 raw not preserved: %s", pts[0])
	}
	if !strings.Contains(string(pts[1]), `"countSum":"10000"`) {
		t.Errorf("row 1 raw not preserved: %s", pts[1])
	}
}

// TestRollUpDaily_NonMidnightBoundIncludesTime covers the explicit --from/--to
// path: a bound off midnight serializes a CivilDateTime.time member, while a
// day-aligned bound omits it.
func TestRollUpDaily_NonMidnightBoundIncludesTime(t *testing.T) {
	var gotBody string
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		b, _ := io.ReadAll(r.Body)
		gotBody = string(b)
		_, _ = w.Write([]byte(`{"rollupDataPoints":[]}`))
	}))
	defer srv.Close()

	c := New(srv.Client(), srv.URL, "users/me", nil)
	steps, _ := LookupDataType("steps")
	from := time.Date(2026, 6, 15, 6, 30, 0, 0, time.UTC)
	to := time.Date(2026, 6, 17, 0, 0, 0, 0, time.UTC)
	if _, err := c.RollUpDaily(context.Background(), steps, from, to); err != nil {
		t.Fatalf("RollUpDaily: %v", err)
	}

	if !strings.Contains(gotBody, `"start":{"date":{"year":2026,"month":6,"day":15},"time":{"hours":6,"minutes":30}}`) {
		t.Errorf("non-midnight start missing time member: %s", gotBody)
	}
	if !strings.Contains(gotBody, `"end":{"date":{"year":2026,"month":6,"day":17}}`) {
		t.Errorf("midnight end should omit time: %s", gotBody)
	}
}

// TestRollUpDaily_ErrorEnvelopeSurfacesViolations checks that an over-long range
// rejection (the real INVALID_ROLLUP_QUERY_DURATION envelope) surfaces the
// actionable BadRequest fieldViolation text, not just "Invalid argument".
func TestRollUpDaily_ErrorEnvelopeSurfacesViolations(t *testing.T) {
	const errBody = `{"error":{"code":400,"message":"Invalid argument in request.","status":"INVALID_ARGUMENT","details":[` +
		`{"@type":"type.googleapis.com/google.rpc.ErrorInfo","reason":"INVALID_ROLLUP_QUERY_DURATION"},` +
		`{"@type":"type.googleapis.com/google.rpc.BadRequest","fieldViolations":[{"field":"range","description":"The duration covered by window_size_days * page_size must not exceed 90 days for steps."}]}` +
		`]}}`
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusBadRequest)
		_, _ = w.Write([]byte(errBody))
	}))
	defer srv.Close()

	c := New(srv.Client(), srv.URL, "users/me", nil)
	steps, _ := LookupDataType("steps")
	_, err := c.RollUpDaily(context.Background(), steps,
		time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC),
		time.Date(2026, 6, 1, 0, 0, 0, 0, time.UTC))
	if err == nil {
		t.Fatal("expected error, got nil")
	}
	var apiErr *Error
	if !errors.As(err, &apiErr) {
		t.Fatalf("error is %T, want *api.Error", err)
	}
	if apiErr.StatusCode != http.StatusBadRequest {
		t.Errorf("StatusCode = %d, want 400", apiErr.StatusCode)
	}
	if !strings.Contains(apiErr.Message, "must not exceed 90 days") {
		t.Errorf("Message = %q, want the field violation detail", apiErr.Message)
	}
	if !strings.Contains(apiErr.Message, "range:") {
		t.Errorf("Message = %q, want the violated field name", apiErr.Message)
	}
}
