package api

import (
	"context"
	"errors"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

func TestListDataPoints_PaginationAndQuery(t *testing.T) {
	page1 := `{"dataPoints":[{"name":"users/me/dataTypes/exercise/dataPoints/1","exercise":{"exerciseType":"ELLIPTICAL"}}],"nextPageToken":"TOK2"}`
	page2 := `{"dataPoints":[{"name":"users/me/dataTypes/exercise/dataPoints/2","exercise":{"exerciseType":"STRENGTH_TRAINING"}}]}`

	var paths, filters, sizes, tokens []string
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		q := r.URL.Query()
		paths = append(paths, r.URL.Path)
		filters = append(filters, q.Get("filter"))
		sizes = append(sizes, q.Get("pageSize"))
		tokens = append(tokens, q.Get("pageToken"))
		w.Header().Set("Content-Type", "application/json")
		if q.Get("pageToken") == "" {
			_, _ = w.Write([]byte(page1))
			return
		}
		_, _ = w.Write([]byte(page2))
	}))
	defer srv.Close()

	c := New(srv.Client(), srv.URL, "users/me", nil)
	from := time.Date(2026, 6, 14, 0, 0, 0, 0, time.UTC)
	to := time.Date(2026, 6, 18, 0, 0, 0, 0, time.UTC)
	exercise, _ := LookupDataType("exercise")

	pts, err := c.ListDataPoints(context.Background(), exercise, from, to, true)
	if err != nil {
		t.Fatalf("ListDataPoints: %v", err)
	}
	if len(pts) != 2 {
		t.Fatalf("got %d points, want 2", len(pts))
	}
	if pts[0].Exercise.ExerciseType != "ELLIPTICAL" || pts[1].Exercise.ExerciseType != "STRENGTH_TRAINING" {
		t.Errorf("unexpected types: %q, %q", pts[0].Exercise.ExerciseType, pts[1].Exercise.ExerciseType)
	}
	// Raw bytes preserved for `sessions --raw`.
	if !strings.Contains(string(pts[0].Raw), `"exerciseType":"ELLIPTICAL"`) {
		t.Errorf("Raw not preserved: %s", pts[0].Raw)
	}

	if len(paths) != 2 {
		t.Fatalf("made %d requests, want 2", len(paths))
	}
	wantPath := "/v4/users/me/dataTypes/exercise/dataPoints"
	for i, p := range paths {
		if p != wantPath {
			t.Errorf("request %d path = %q, want %q", i, p, wantPath)
		}
		if sizes[i] != "25" {
			t.Errorf("request %d pageSize = %q, want 25", i, sizes[i])
		}
	}
	wantFilter := `exercise.interval.civil_start_time >= "2026-06-14T00:00:00" AND exercise.interval.civil_start_time < "2026-06-18T00:00:00"`
	if filters[0] != wantFilter {
		t.Errorf("filter = %q, want %q", filters[0], wantFilter)
	}
	if tokens[0] != "" || tokens[1] != "TOK2" {
		t.Errorf("pageTokens = %q, %q; want \"\", \"TOK2\"", tokens[0], tokens[1])
	}
}

func TestListDataPoints_ErrorEnvelope(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusForbidden)
		_, _ = w.Write([]byte(`{"error":{"code":403,"message":"Request had insufficient authentication scopes.","status":"PERMISSION_DENIED"}}`))
	}))
	defer srv.Close()

	c := New(srv.Client(), srv.URL, "users/me", nil)
	exercise, _ := LookupDataType("exercise")
	_, err := c.ListDataPoints(context.Background(), exercise,
		time.Date(2026, 6, 14, 0, 0, 0, 0, time.UTC),
		time.Date(2026, 6, 18, 0, 0, 0, 0, time.UTC), true)
	if err == nil {
		t.Fatal("expected error, got nil")
	}
	var apiErr *Error
	if !errors.As(err, &apiErr) {
		t.Fatalf("error is %T, want *api.Error", err)
	}
	if apiErr.StatusCode != http.StatusForbidden {
		t.Errorf("StatusCode = %d, want 403", apiErr.StatusCode)
	}
	if !strings.Contains(apiErr.Message, "insufficient authentication scopes") {
		t.Errorf("Message = %q, want Google envelope message", apiErr.Message)
	}
}

// TestRawGet_RejectsPathsOutsideV4Surface is the immutable guard for the
// description/behavior-mismatch finding: `api get` advertises a read-only v4 GET,
// so RawGet must reject anything outside the v4 surface — non-v4 paths, absolute
// URLs, "//authority" smuggling, and ".." traversal — and crucially must make NO
// network call when it does. A real v4 path still reaches the server. Fix a
// failure by tightening validateRawPath, never by loosening this test.
func TestRawGet_RejectsPathsOutsideV4Surface(t *testing.T) {
	var hits int
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		hits++
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"ok":true}`))
	}))
	defer srv.Close()
	c := New(srv.Client(), srv.URL, "users/me", nil)

	rejected := []string{
		"",                                // empty
		"   ",                             // blank
		"/",                               // root, no v4
		"v3/users/me",                     // wrong version
		"/admin/users",                    // non-v4 endpoint
		"users/me/profile",                // missing v4 prefix
		"http://evil.example/v4/users/me", // absolute URL (scheme)
		"//evil.example/v4/users/me",      // protocol-relative authority
		"v4/../../admin",                  // parent traversal out of v4
		"/v4/users/../../secret",          // traversal mid-path
	}
	for _, p := range rejected {
		_, err := c.RawGet(context.Background(), p)
		if err == nil {
			t.Errorf("RawGet(%q) = nil error, want rejection", p)
			continue
		}
		if !errors.Is(err, ErrPathNotAllowed) {
			t.Errorf("RawGet(%q) error = %v, want ErrPathNotAllowed", p, err)
		}
	}
	if hits != 0 {
		t.Errorf("rejected paths made %d network request(s), want 0 (validation must precede the call)", hits)
	}

	// A genuine read-only v4 path is allowed and reaches the server.
	body, err := c.RawGet(context.Background(), "/v4/users/me/profile")
	if err != nil {
		t.Fatalf("RawGet(valid v4 path) = %v, want success", err)
	}
	if !strings.Contains(string(body), `"ok":true`) {
		t.Errorf("unexpected body for valid path: %s", body)
	}
	if hits != 1 {
		t.Errorf("valid v4 path made %d network request(s), want 1", hits)
	}
}

func TestListDataPoints_Empty(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		_, _ = w.Write([]byte(`{}`)) // no dataPoints key at all.
	}))
	defer srv.Close()

	c := New(srv.Client(), srv.URL, "users/me", nil)
	exercise, _ := LookupDataType("exercise")
	pts, err := c.ListDataPoints(context.Background(), exercise,
		time.Date(2026, 6, 14, 0, 0, 0, 0, time.UTC),
		time.Date(2026, 6, 18, 0, 0, 0, 0, time.UTC), true)
	if err != nil {
		t.Fatalf("ListDataPoints: %v", err)
	}
	if len(pts) != 0 {
		t.Errorf("got %d points, want 0", len(pts))
	}
}
