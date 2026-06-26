package doctor

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/maxtechera/admirarr/internal/config"
	"github.com/spf13/viper"
)

// mockServiceMux creates a handler that responds to common *Arr API endpoints.
func mockServiceMux(apiVer string) http.Handler {
	mux := http.NewServeMux()

	// Health endpoint
	mux.HandleFunc("/api/"+apiVer+"/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode([]struct{}{})
	})

	// System status
	mux.HandleFunc("/api/"+apiVer+"/system/status", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{"version": "5.0.0"})
	})

	// Root folders
	mux.HandleFunc("/api/"+apiVer+"/rootfolder", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode([]map[string]interface{}{
			{"id": 1, "path": "/data/media/movies", "accessible": true, "freeSpace": 500000000000},
		})
	})

	return mux
}

// configureTestService points a service to the test server.
func configureTestService(t *testing.T, service string, ts *httptest.Server) {
	t.Helper()
	addr := strings.TrimPrefix(ts.URL, "http://")
	parts := strings.SplitN(addr, ":", 2)
	var port int
	if len(parts) == 2 {
		for i, ch := range parts[1] {
			if ch < '0' || ch > '9' {
				parts[1] = parts[1][:i]
				break
			}
		}
		for _, ch := range parts[1] {
			port = port*10 + int(ch-'0')
		}
	}

	viper.Set("services."+service+".host", parts[0])
	viper.Set("services."+service+".port", port)
	// Set API version from registry if available
	if def, ok := config.GetServiceDef(service); ok && def.APIVer != "" {
		viper.Set("services."+service+".api_ver", def.APIVer)
	}
}

func TestResult_Init(t *testing.T) {
	r := &Result{}
	if r.ChecksPassed != 0 || len(r.Issues) != 0 {
		t.Error("new Result should start at zero")
	}
}

func TestCheckConnectivity_WithMockServer(t *testing.T) {
	viper.Reset()

	// Create a mock server for radarr
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(200)
		w.Write([]byte(`[]`))
	}))
	defer ts.Close()

	configureTestService(t, "radarr", ts)

	// Point all other services with ports to unreachable addresses
	for _, name := range config.AllServiceNames() {
		if name == "radarr" {
			continue
		}
		def, ok := config.GetServiceDef(name)
		if !ok || def.Port == 0 {
			continue
		}
		viper.Set("services."+name+".host", "127.0.0.1")
		viper.Set("services."+name+".port", 1)
	}

	config.Load()

	r := &Result{}
	checkConnectivity(r)

	// Radarr should pass, others should fail
	if r.ChecksPassed < 1 {
		t.Error("expected at least 1 check passed (radarr mock)")
	}
}

func TestCheckMediaPaths_WithMockServer(t *testing.T) {
	viper.Reset()

	// Mock radarr with root folders and download clients
	radarrMux := http.NewServeMux()
	radarrMux.HandleFunc("/api/v3/rootfolder", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode([]map[string]interface{}{
			{"id": 1, "path": "/data/media/movies", "accessible": true, "freeSpace": 500000000000},
		})
	})
	radarrMux.HandleFunc("/api/v3/downloadclient", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode([]map[string]interface{}{
			{"id": 1, "name": "qBittorrent", "enable": true, "implementation": "QBittorrent",
				"fields": []map[string]interface{}{
					{"name": "host", "value": "localhost"},
					{"name": "port", "value": 8080},
					{"name": "movieCategory", "value": "movies"},
				}},
		})
	})
	// Health endpoint for reachability check
	radarrMux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(200)
		w.Write([]byte(`[]`))
	})
	radarrTS := httptest.NewServer(radarrMux)
	defer radarrTS.Close()

	sonarrMux := http.NewServeMux()
	sonarrMux.HandleFunc("/api/v3/rootfolder", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode([]map[string]interface{}{
			{"id": 1, "path": "/data/media/tv", "accessible": true, "freeSpace": 500000000000},
		})
	})
	sonarrMux.HandleFunc("/api/v3/downloadclient", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode([]map[string]interface{}{
			{"id": 1, "name": "qBittorrent", "enable": true, "implementation": "QBittorrent",
				"fields": []map[string]interface{}{
					{"name": "host", "value": "localhost"},
					{"name": "port", "value": 8080},
					{"name": "tvCategory", "value": "tv-sonarr"},
				}},
		})
	})
	sonarrMux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(200)
		w.Write([]byte(`[]`))
	})
	sonarrTS := httptest.NewServer(sonarrMux)
	defer sonarrTS.Close()

	configureTestService(t, "radarr", radarrTS)
	configureTestService(t, "sonarr", sonarrTS)
	config.Load()

	r := &Result{}
	checkMediaPaths(r)

	// Should pass: 2 root folders + 2 download clients = at least 4 checks
	if r.ChecksPassed < 4 {
		t.Errorf("expected at least 4 pipeline checks passed, got %d (issues: %v)", r.ChecksPassed, r.Issues)
	}
}

func TestCheckServiceWarnings_NoWarnings(t *testing.T) {
	viper.Reset()

	// Create mock servers that return empty health arrays
	mux := http.NewServeMux()
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`[]`))
	})

	ts := httptest.NewServer(mux)
	defer ts.Close()

	for _, svc := range []string{"radarr", "sonarr", "prowlarr"} {
		configureTestService(t, svc, ts)
	}
	config.Load()

	r := &Result{}
	checkServiceWarnings(r)

	if r.ChecksPassed != 1 {
		t.Errorf("expected 1 check passed (no warnings), got %d", r.ChecksPassed)
	}
}

func TestCheckServiceWarnings_WithWarnings(t *testing.T) {
	viper.Reset()

	mux := http.NewServeMux()
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode([]map[string]string{
			{"type": "warning", "message": "Root folder is not accessible", "source": "RootFolderCheck"},
		})
	})

	ts := httptest.NewServer(mux)
	defer ts.Close()

	for _, svc := range []string{"radarr", "sonarr", "prowlarr"} {
		configureTestService(t, svc, ts)
	}
	config.Load()

	r := &Result{}
	checkServiceWarnings(r)

	if len(r.Issues) == 0 {
		t.Error("expected issues from health warnings")
	}
}

func TestCheckIndexers_WithMockProwlarr(t *testing.T) {
	viper.Reset()

	mux := http.NewServeMux()
	mux.HandleFunc("/api/v1/indexer", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode([]map[string]interface{}{
			{"id": 1, "name": "1337x", "enable": true},
			{"id": 2, "name": "TorrentGalaxy", "enable": true},
			{"id": 3, "name": "Disabled Indexer", "enable": false},
		})
	})
	mux.HandleFunc("/api/v1/indexerstatus", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode([]map[string]interface{}{
			{"indexerId": 2, "mostRecentFailure": "2026-03-10T12:00:00Z"},
		})
	})

	ts := httptest.NewServer(mux)
	defer ts.Close()

	configureTestService(t, "prowlarr", ts)
	config.Load()

	r := &Result{}
	checkIndexers(r)

	// 1 healthy should pass, 1 failing should be an issue
	if r.ChecksPassed < 1 {
		t.Error("expected at least 1 check passed for healthy indexers")
	}
	hasIndexerIssue := false
	for _, issue := range r.Issues {
		if strings.Contains(issue.Description, "INDEXERS FAILING") {
			hasIndexerIssue = true
			break
		}
	}
	if !hasIndexerIssue {
		t.Error("expected failing indexer issue")
	}
}
