package cmd

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/qbit"
	"github.com/spf13/viper"
)

// ── Helpers ──

// setupMockService points a service to a test server in viper config.
func setupMockService(t *testing.T, service string, ts *httptest.Server) {
	t.Helper()
	addr := strings.TrimPrefix(ts.URL, "http://")
	parts := strings.SplitN(addr, ":", 2)
	var port int
	fmt.Sscanf(parts[1], "%d", &port)

	viper.Set("services."+service+".host", parts[0])
	viper.Set("services."+service+".port", port)
	viper.Set("services."+service+".type", "docker")
	switch service {
	case "radarr", "sonarr":
		viper.Set("services."+service+".api_ver", "v3")
	case "prowlarr":
		viper.Set("services."+service+".api_ver", "v1")
	}
}

// pointToUnreachable makes a service unreachable for tests.
func pointToUnreachable(services ...string) {
	for _, svc := range services {
		viper.Set("services."+svc+".host", "127.0.0.1")
		viper.Set("services."+svc+".port", 1)
		viper.Set("services."+svc+".type", "docker")
	}
}

// ── Data type tests ──

func TestStatusIndexer_JSONParsing(t *testing.T) {
	raw := `[{"name":"1337x","enable":true},{"name":"YTS","enable":false}]`
	var indexers []statusIndexer
	if err := json.Unmarshal([]byte(raw), &indexers); err != nil {
		t.Fatalf("failed to unmarshal: %v", err)
	}
	if len(indexers) != 2 {
		t.Fatalf("expected 2 indexers, got %d", len(indexers))
	}
	if indexers[0].Name != "1337x" || !indexers[0].Enable {
		t.Errorf("indexer 0: got %+v", indexers[0])
	}
	if indexers[1].Name != "YTS" || indexers[1].Enable {
		t.Errorf("indexer 1: got %+v", indexers[1])
	}
}

func TestMovieInfo_JSONParsing(t *testing.T) {
	raw := `{"hasFile":true,"monitored":true,"sizeOnDisk":1500000000}`
	var m arr.Movie
	if err := json.Unmarshal([]byte(raw), &m); err != nil {
		t.Fatalf("failed to unmarshal: %v", err)
	}
	if !m.HasFile || !m.Monitored || m.SizeOnDisk != 1500000000 {
		t.Errorf("unexpected movie: %+v", m)
	}
}

func TestSeriesInfo_JSONParsing(t *testing.T) {
	raw := `{"statistics":{"episodeCount":24,"episodeFileCount":12,"sizeOnDisk":5000000000}}`
	var s arr.Series
	if err := json.Unmarshal([]byte(raw), &s); err != nil {
		t.Fatalf("failed to unmarshal: %v", err)
	}
	if s.Statistics.EpisodeCount != 24 || s.Statistics.EpisodeFileCount != 12 {
		t.Errorf("unexpected series: %+v", s.Statistics)
	}
}

func TestQueueRecord_JSONParsing(t *testing.T) {
	raw := `{"title":"Movie.2026.1080p","trackedDownloadState":"downloading","sizeleft":500.5,"size":1500.0}`
	var q arr.QueueRecord
	if err := json.Unmarshal([]byte(raw), &q); err != nil {
		t.Fatalf("failed to unmarshal: %v", err)
	}
	if q.Title != "Movie.2026.1080p" || q.TrackedDownloadState != "downloading" {
		t.Errorf("unexpected queue record: %+v", q)
	}
	if q.Size != 1500.0 || q.Sizeleft != 500.5 {
		t.Errorf("unexpected sizes: size=%f sizeleft=%f", q.Size, q.Sizeleft)
	}
}

func TestTorrentInfo_JSONParsing(t *testing.T) {
	raw := `{"name":"ubuntu-24.04.iso","size":4000000000,"progress":0.75,"dlspeed":5242880,"state":"downloading","eta":120}`
	var ti qbit.Torrent
	if err := json.Unmarshal([]byte(raw), &ti); err != nil {
		t.Fatalf("failed to unmarshal: %v", err)
	}
	if ti.Progress != 0.75 || ti.DLSpeed != 5242880 || ti.ETA != 120 {
		t.Errorf("unexpected torrent: %+v", ti)
	}
}

// ── Indexer comparison logic ──

func TestIndexerComparison_AllPresent(t *testing.T) {
	// Build a set matching all recommended indexers
	configured := make(map[string]bool)
	for _, rec := range recommendedIndexers {
		configured[strings.ToLower(rec.Name)] = true
	}

	var missing []string
	for _, rec := range recommendedIndexers {
		if !configured[strings.ToLower(rec.Name)] {
			missing = append(missing, rec.Name)
		}
	}
	if len(missing) != 0 {
		t.Errorf("expected 0 missing, got %v", missing)
	}
}

func TestIndexerComparison_SomeMissing(t *testing.T) {
	// Only configure 3 of the recommended indexers
	configured := map[string]bool{
		"1337x": true,
		"yts":   true,
		"eztv":  true,
	}

	var missing []string
	for _, rec := range recommendedIndexers {
		if !configured[strings.ToLower(rec.Name)] {
			missing = append(missing, rec.Name)
		}
	}

	have := len(recommendedIndexers) - len(missing)
	if have != 3 {
		t.Errorf("expected 3 configured, got %d", have)
	}
	if len(missing) != 7 {
		t.Errorf("expected 7 missing, got %d: %v", len(missing), missing)
	}
}

func TestIndexerComparison_CaseInsensitive(t *testing.T) {
	// Prowlarr may return names with different casing
	configured := map[string]bool{
		"the pirate bay": true,
		"nyaa.si":        true,
	}

	found := 0
	for _, rec := range recommendedIndexers {
		if configured[strings.ToLower(rec.Name)] {
			found++
		}
	}
	if found != 2 {
		t.Errorf("expected 2 matches with case-insensitive comparison, got %d", found)
	}
}

func TestIndexerComparison_NoneConfigured(t *testing.T) {
	configured := make(map[string]bool)

	var missing []string
	for _, rec := range recommendedIndexers {
		if !configured[strings.ToLower(rec.Name)] {
			missing = append(missing, rec.Name)
		}
	}
	if len(missing) != len(recommendedIndexers) {
		t.Errorf("expected all %d missing, got %d", len(recommendedIndexers), len(missing))
	}
}

func TestIndexerEnabledDisabledCount(t *testing.T) {
	indexers := []statusIndexer{
		{Name: "1337x", Enable: true},
		{Name: "YTS", Enable: true},
		{Name: "EZTV", Enable: false},
		{Name: "Knaben", Enable: true},
		{Name: "Custom", Enable: false},
	}

	enabled, disabled := 0, 0
	for _, idx := range indexers {
		if idx.Enable {
			enabled++
		} else {
			disabled++
		}
	}
	if enabled != 3 {
		t.Errorf("expected 3 enabled, got %d", enabled)
	}
	if disabled != 2 {
		t.Errorf("expected 2 disabled, got %d", disabled)
	}
}

// ── RecommendedIndexers registry ──

func TestRecommendedIndexers_HasExpectedCount(t *testing.T) {
	if len(recommendedIndexers) != 10 {
		t.Errorf("expected 10 recommended indexers, got %d", len(recommendedIndexers))
	}
}

func TestRecommendedIndexers_AllHaveCategory(t *testing.T) {
	validCategories := map[string]bool{"general": true, "movies": true, "tv": true, "anime": true}
	for _, idx := range recommendedIndexers {
		if !validCategories[idx.Category] {
			t.Errorf("indexer %q has invalid category %q", idx.Name, idx.Category)
		}
	}
}

func TestRecommendedIndexers_AllHaveImplementation(t *testing.T) {
	for _, idx := range recommendedIndexers {
		if idx.Implementation == "" {
			t.Errorf("indexer %q has no implementation", idx.Name)
		}
		if idx.ConfigContract == "" {
			t.Errorf("indexer %q has no config contract", idx.Name)
		}
	}
}

func TestRecommendedIndexers_NoDuplicateNames(t *testing.T) {
	seen := make(map[string]bool)
	for _, idx := range recommendedIndexers {
		lower := strings.ToLower(idx.Name)
		if seen[lower] {
			t.Errorf("duplicate indexer name: %q", idx.Name)
		}
		seen[lower] = true
	}
}

// ── DashData with mock services ──

func TestDashData_IndexerFetch(t *testing.T) {
	viper.Reset()

	// Mock Prowlarr returning indexers
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v1/indexer", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode([]statusIndexer{
			{Name: "1337x", Enable: true},
			{Name: "YTS", Enable: true},
			{Name: "EZTV", Enable: false},
		})
	})
	mux.HandleFunc("/api/v1/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`[]`))
	})
	ts := httptest.NewServer(mux)
	defer ts.Close()

	setupMockService(t, "prowlarr", ts)

	// Make all other services unreachable
	pointToUnreachable("radarr", "sonarr", "plex", "qbittorrent",
		"tautulli", "seerr", "bazarr", "flaresolverr",
		"jellyfin", "gluetun", "autobrr", "maintainerr")

	config.Load()

	// Fetch indexers via the API client
	var indexers []statusIndexer
	err := api.GetJSON("prowlarr", "api/v1/indexer", nil, &indexers)
	if err != nil {
		t.Fatalf("failed to fetch indexers: %v", err)
	}
	if len(indexers) != 3 {
		t.Fatalf("expected 3 indexers, got %d", len(indexers))
	}
	if indexers[0].Name != "1337x" || !indexers[0].Enable {
		t.Errorf("indexer 0: got %+v", indexers[0])
	}
	if indexers[2].Name != "EZTV" || indexers[2].Enable {
		t.Errorf("indexer 2 should be disabled: got %+v", indexers[2])
	}
}

// ── fmtETA (existing, extended) ──

func TestFmtETA_EdgeCases(t *testing.T) {
	tests := []struct {
		secs     int64
		expected string
	}{
		{0, ""},
		{-100, ""},
		{1, "1s"},
		{59, "59s"},
		{60, "1m0s"},
		{61, "1m1s"},
		{3599, "59m59s"},
		{3600, "1h0m"},
		{86400, "24h0m"},
		{8640000, "2400h0m"},
		{8640001, ""},
	}
	for _, tt := range tests {
		got := fmtETA(tt.secs)
		if got != tt.expected {
			t.Errorf("fmtETA(%d) = %q, want %q", tt.secs, got, tt.expected)
		}
	}
}

// ── DashData library calculations ──

func TestDashData_MovieStats(t *testing.T) {
	movies := []arr.Movie{
		{HasFile: true, Monitored: true, SizeOnDisk: 5000000000},
		{HasFile: true, Monitored: true, SizeOnDisk: 3000000000},
		{HasFile: false, Monitored: true, SizeOnDisk: 0},
		{HasFile: false, Monitored: false, SizeOnDisk: 0}, // unmonitored, shouldn't count as missing
	}

	have, missing := 0, 0
	var totalSize int64
	for _, m := range movies {
		if m.HasFile {
			have++
		}
		if m.Monitored && !m.HasFile {
			missing++
		}
		totalSize += m.SizeOnDisk
	}

	if have != 2 {
		t.Errorf("expected 2 on disk, got %d", have)
	}
	if missing != 1 {
		t.Errorf("expected 1 missing, got %d", missing)
	}
	if totalSize != 8000000000 {
		t.Errorf("expected 8GB total, got %d", totalSize)
	}
}

func TestDashData_SeriesStats(t *testing.T) {
	series := []arr.Series{
		{Statistics: arr.SeriesStats{EpisodeCount: 24, EpisodeFileCount: 20, SizeOnDisk: 10000000000}},
		{Statistics: arr.SeriesStats{EpisodeCount: 12, EpisodeFileCount: 12, SizeOnDisk: 5000000000}},
	}

	totalEps, haveEps := 0, 0
	var totalSize int64
	for _, s := range series {
		totalEps += s.Statistics.EpisodeCount
		haveEps += s.Statistics.EpisodeFileCount
		totalSize += s.Statistics.SizeOnDisk
	}

	if totalEps != 36 {
		t.Errorf("expected 36 total episodes, got %d", totalEps)
	}
	if haveEps != 32 {
		t.Errorf("expected 32 episodes on disk, got %d", haveEps)
	}
	if totalSize != 15000000000 {
		t.Errorf("expected 15GB, got %d", totalSize)
	}
}

// ── Torrent state classification ──

func TestTorrentStateClassification(t *testing.T) {
	dlStates := map[string]bool{"downloading": true, "stalledDL": true, "forcedDL": true, "metaDL": true}
	seedStates := map[string]bool{"uploading": true, "stalledUP": true, "forcedUP": true}

	torrents := []qbit.Torrent{
		{State: "downloading", DLSpeed: 1048576},
		{State: "downloading", DLSpeed: 2097152},
		{State: "stalledDL", DLSpeed: 0},
		{State: "uploading", DLSpeed: 0},
		{State: "stalledUP", DLSpeed: 0},
		{State: "pausedUP", DLSpeed: 0},
	}

	var dlCount, seedCount int
	var totalDL int64
	for _, torr := range torrents {
		if dlStates[torr.State] {
			dlCount++
			totalDL += torr.DLSpeed
		}
		if seedStates[torr.State] {
			seedCount++
		}
	}

	if dlCount != 3 {
		t.Errorf("expected 3 downloading, got %d", dlCount)
	}
	if seedCount != 2 {
		t.Errorf("expected 2 seeding, got %d", seedCount)
	}
	if totalDL != 3145728 {
		t.Errorf("expected 3145728 total DL speed, got %d", totalDL)
	}
}

// ── Queue progress calculation ──

func TestQueueProgressCalculation(t *testing.T) {
	tests := []struct {
		size     float64
		sizeleft float64
		expected float64
	}{
		{1500.0, 500.0, 66},  // ~66%
		{1000.0, 0.0, 100},   // 100%
		{1000.0, 1000.0, 0},  // 0%
		{0.0, 0.0, 0},        // edge case: no size
	}

	for _, tt := range tests {
		var pct float64
		if tt.size > 0 {
			pct = (1 - tt.sizeleft/tt.size) * 100
		}
		// Allow 1% tolerance for float comparison
		if pct < tt.expected-1 || pct > tt.expected+1 {
			t.Errorf("size=%f sizeleft=%f: expected ~%.0f%%, got %.0f%%",
				tt.size, tt.sizeleft, tt.expected, pct)
		}
	}
}

// ── Disk percentage calculation ──

func TestDiskPercentage(t *testing.T) {
	tests := []struct {
		total    int64
		free     int64
		expected float64
	}{
		{1000000000000, 150000000000, 85},  // 85%
		{1000000000000, 50000000000, 95},   // 95%
		{1000000000000, 500000000000, 50},  // 50%
		{1000000000000, 1000000000000, 0},  // 0%
	}

	for _, tt := range tests {
		used := tt.total - tt.free
		pct := float64(used) / float64(tt.total) * 100
		if pct < tt.expected-1 || pct > tt.expected+1 {
			t.Errorf("total=%d free=%d: expected ~%.0f%%, got %.0f%%",
				tt.total, tt.free, tt.expected, pct)
		}
	}
}
