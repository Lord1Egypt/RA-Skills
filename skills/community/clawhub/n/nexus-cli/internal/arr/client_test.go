package arr

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/maxtechera/admirarr/internal/config"
	"github.com/spf13/viper"
)

// setupRadarr creates a test server and configures viper so arr.New("radarr") hits it.
// Returns the server (caller must defer ts.Close()) and a ready client.
func setupRadarr(t *testing.T, handler http.Handler) (*httptest.Server, *Client) {
	t.Helper()
	ts := httptest.NewServer(handler)
	injectService(t, "radarr", ts.URL, "v3")
	return ts, New("radarr")
}

// setupSonarr creates a test server for sonarr.
func setupSonarr(t *testing.T, handler http.Handler) (*httptest.Server, *Client) {
	t.Helper()
	ts := httptest.NewServer(handler)
	injectService(t, "sonarr", ts.URL, "v3")
	return ts, New("sonarr")
}

// setupProwlarr creates a test server for prowlarr.
func setupProwlarr(t *testing.T, handler http.Handler) (*httptest.Server, *Client) {
	t.Helper()
	ts := httptest.NewServer(handler)
	injectService(t, "prowlarr", ts.URL, "v1")
	return ts, New("prowlarr")
}

func injectService(t *testing.T, name, rawURL, apiVer string) {
	t.Helper()
	addr := strings.TrimPrefix(rawURL, "http://")
	parts := strings.SplitN(addr, ":", 2)
	var port int
	fmt.Sscanf(parts[1], "%d", &port)
	viper.Set("services."+name+".host", parts[0])
	viper.Set("services."+name+".port", port)
	viper.Set("services."+name+".api_ver", apiVer)
	config.Load()
}

// --- Radarr ---

func TestMovies(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v3/movie", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode([]Movie{
			{ID: 1, Title: "Inception", Year: 2010, HasFile: true, SizeOnDisk: 5_000_000_000},
			{ID: 2, Title: "The Matrix", Year: 1999, HasFile: false, Monitored: true},
		})
	})

	ts, client := setupRadarr(t, mux)
	defer ts.Close()

	movies, err := client.Movies()
	if err != nil {
		t.Fatalf("Movies() failed: %v", err)
	}
	if len(movies) != 2 {
		t.Fatalf("expected 2 movies, got %d", len(movies))
	}
	if movies[0].Title != "Inception" || movies[0].Year != 2010 {
		t.Errorf("unexpected movie[0]: %+v", movies[0])
	}
	if movies[1].HasFile {
		t.Error("expected movie[1] hasFile=false")
	}
}

func TestLookupMovie(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v3/movie/lookup", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Query().Get("term") != "inception" {
			t.Errorf("expected term=inception, got %s", r.URL.Query().Get("term"))
		}
		json.NewEncoder(w).Encode([]map[string]interface{}{
			{"title": "Inception", "year": 2010},
		})
	})

	ts, client := setupRadarr(t, mux)
	defer ts.Close()

	results, err := client.LookupMovie("inception")
	if err != nil {
		t.Fatalf("LookupMovie() failed: %v", err)
	}
	if len(results) != 1 {
		t.Fatalf("expected 1 result, got %d", len(results))
	}
	if results[0]["title"] != "Inception" {
		t.Errorf("unexpected title: %v", results[0]["title"])
	}
}

func TestAddMovie(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v3/movie", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			t.Errorf("expected POST, got %s", r.Method)
		}
		body, _ := io.ReadAll(r.Body)
		var payload map[string]interface{}
		json.Unmarshal(body, &payload)
		if payload["title"] != "Inception" {
			t.Errorf("expected title=Inception, got %v", payload["title"])
		}
		w.Write([]byte(`{"id":42}`))
	})

	ts, client := setupRadarr(t, mux)
	defer ts.Close()

	result, err := client.AddMovie(map[string]interface{}{"title": "Inception"})
	if err != nil {
		t.Fatalf("AddMovie() failed: %v", err)
	}
	if result["id"] != float64(42) {
		t.Errorf("expected id=42, got %v", result["id"])
	}
}

func TestReleases(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v3/release", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Query().Get("movieId") != "5" {
			t.Errorf("expected movieId=5, got %s", r.URL.Query().Get("movieId"))
		}
		json.NewEncoder(w).Encode([]Release{
			{Title: "Inception.2010.1080p", Size: 2_000_000_000, Seeders: 50},
		})
	})

	ts, client := setupRadarr(t, mux)
	defer ts.Close()

	releases, err := client.Releases(5)
	if err != nil {
		t.Fatalf("Releases() failed: %v", err)
	}
	if len(releases) != 1 || releases[0].Seeders != 50 {
		t.Errorf("unexpected releases: %+v", releases)
	}
}

// --- Sonarr ---

func TestSeries(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v3/series", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode([]Series{
			{ID: 1, Title: "Breaking Bad", Year: 2008, Statistics: SeriesStats{EpisodeCount: 62, EpisodeFileCount: 62, SizeOnDisk: 100_000_000_000}},
			{ID: 2, Title: "The Wire", Year: 2002, Monitored: true},
		})
	})

	ts, client := setupSonarr(t, mux)
	defer ts.Close()

	series, err := client.Series()
	if err != nil {
		t.Fatalf("Series() failed: %v", err)
	}
	if len(series) != 2 {
		t.Fatalf("expected 2 series, got %d", len(series))
	}
	if series[0].Statistics.EpisodeCount != 62 {
		t.Errorf("expected 62 episodes, got %d", series[0].Statistics.EpisodeCount)
	}
}

func TestWantedMissing(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v3/wanted/missing", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Query().Get("pageSize") != "20" {
			t.Errorf("expected pageSize=20, got %s", r.URL.Query().Get("pageSize"))
		}
		if r.URL.Query().Get("sortKey") != "airDateUtc" {
			t.Errorf("expected sortKey=airDateUtc, got %s", r.URL.Query().Get("sortKey"))
		}
		json.NewEncoder(w).Encode(WantedMissingPage{
			TotalRecords: 1,
			Records: []MissingEpisode{
				{Title: "Pilot", SeasonNumber: 1, EpisodeNumber: 1, Series: struct {
					Title string `json:"title"`
				}{Title: "Breaking Bad"}},
			},
		})
	})

	ts, client := setupSonarr(t, mux)
	defer ts.Close()

	page, err := client.WantedMissing(20, map[string]string{"sortKey": "airDateUtc"})
	if err != nil {
		t.Fatalf("WantedMissing() failed: %v", err)
	}
	if page.TotalRecords != 1 {
		t.Errorf("expected 1 total, got %d", page.TotalRecords)
	}
	if page.Records[0].Series.Title != "Breaking Bad" {
		t.Errorf("unexpected series title: %s", page.Records[0].Series.Title)
	}
}

// --- Shared endpoints ---

func TestQueue(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v3/queue", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Query().Get("pageSize") != "50" {
			t.Errorf("expected pageSize=50, got %s", r.URL.Query().Get("pageSize"))
		}
		json.NewEncoder(w).Encode(QueuePage{
			TotalRecords: 2,
			Records: []QueueRecord{
				{Title: "Inception", TrackedDownloadState: "importPending", Size: 2000, Sizeleft: 500},
				{Title: "The Matrix", TrackedDownloadState: "downloading", Size: 3000, Sizeleft: 1500},
			},
		})
	})

	ts, client := setupRadarr(t, mux)
	defer ts.Close()

	page, err := client.Queue(50)
	if err != nil {
		t.Fatalf("Queue() failed: %v", err)
	}
	if page.TotalRecords != 2 {
		t.Fatalf("expected 2 total, got %d", page.TotalRecords)
	}
	if page.Records[0].TrackedDownloadState != "importPending" {
		t.Errorf("unexpected state: %s", page.Records[0].TrackedDownloadState)
	}
}

func TestHealth(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v3/health", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode([]HealthItem{
			{Type: "warning", Message: "No root folders configured", Source: "RootFolderCheck"},
		})
	})

	ts, client := setupRadarr(t, mux)
	defer ts.Close()

	items, err := client.Health()
	if err != nil {
		t.Fatalf("Health() failed: %v", err)
	}
	if len(items) != 1 || items[0].Type != "warning" {
		t.Errorf("unexpected health: %+v", items)
	}
}

func TestRootFolders(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v3/rootfolder", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode([]RootFolder{
			{ID: 1, Path: "/data/media/movies", Accessible: true, FreeSpace: 500_000_000_000},
		})
	})

	ts, client := setupRadarr(t, mux)
	defer ts.Close()

	folders, err := client.RootFolders()
	if err != nil {
		t.Fatalf("RootFolders() failed: %v", err)
	}
	if len(folders) != 1 || !folders[0].Accessible {
		t.Errorf("unexpected folders: %+v", folders)
	}
}

func TestAddRootFolder(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v3/rootfolder", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			t.Errorf("expected POST, got %s", r.Method)
		}
		body, _ := io.ReadAll(r.Body)
		var payload map[string]string
		json.Unmarshal(body, &payload)
		if payload["path"] != "/data/media/movies" {
			t.Errorf("expected path=/data/media/movies, got %s", payload["path"])
		}
		w.Write([]byte(`{"id":1}`))
	})

	ts, client := setupRadarr(t, mux)
	defer ts.Close()

	if err := client.AddRootFolder("/data/media/movies"); err != nil {
		t.Fatalf("AddRootFolder() failed: %v", err)
	}
}

func TestQualityProfiles(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v3/qualityprofile", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode([]QualityProfile{
			{ID: 1, Name: "HD-1080p"},
			{ID: 2, Name: "Ultra-HD"},
		})
	})

	ts, client := setupRadarr(t, mux)
	defer ts.Close()

	profiles, err := client.QualityProfiles()
	if err != nil {
		t.Fatalf("QualityProfiles() failed: %v", err)
	}
	if len(profiles) != 2 || profiles[0].Name != "HD-1080p" {
		t.Errorf("unexpected profiles: %+v", profiles)
	}
}

func TestCommands(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v3/command", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode([]Command{
			{Name: "RefreshMovie", Status: "started"},
		})
	})

	ts, client := setupRadarr(t, mux)
	defer ts.Close()

	cmds, err := client.Commands()
	if err != nil {
		t.Fatalf("Commands() failed: %v", err)
	}
	if len(cmds) != 1 || cmds[0].Name != "RefreshMovie" {
		t.Errorf("unexpected commands: %+v", cmds)
	}
}

// --- Prowlarr ---

func TestSearch(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v1/search", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Query().Get("query") != "inception" {
			t.Errorf("expected query=inception, got %s", r.URL.Query().Get("query"))
		}
		if r.URL.Query().Get("type") != "search" {
			t.Errorf("expected type=search, got %s", r.URL.Query().Get("type"))
		}
		json.NewEncoder(w).Encode([]SearchResult{
			{Title: "Inception.2010.1080p", Size: 2_000_000_000, Seeders: 100, Indexer: "1337x"},
		})
	})

	ts, client := setupProwlarr(t, mux)
	defer ts.Close()

	results, err := client.Search("inception")
	if err != nil {
		t.Fatalf("Search() failed: %v", err)
	}
	if len(results) != 1 || results[0].Seeders != 100 {
		t.Errorf("unexpected results: %+v", results)
	}
}

func TestIndexers(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v1/indexer", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode([]Indexer{
			{ID: 1, Name: "1337x", Enable: true, Protocol: "torrent"},
			{ID: 2, Name: "NZBgeek", Enable: false, Protocol: "usenet"},
		})
	})

	ts, client := setupProwlarr(t, mux)
	defer ts.Close()

	indexers, err := client.Indexers()
	if err != nil {
		t.Fatalf("Indexers() failed: %v", err)
	}
	if len(indexers) != 2 {
		t.Fatalf("expected 2 indexers, got %d", len(indexers))
	}
	if indexers[0].Name != "1337x" || !indexers[0].Enable {
		t.Errorf("unexpected indexer[0]: %+v", indexers[0])
	}
}

func TestIndexerStatuses(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v1/indexerstatus", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode([]IndexerStatus{
			{IndexerID: 1, MostRecentFailure: "2026-01-01T00:00:00Z", DisabledTill: "2026-01-01T01:00:00Z"},
		})
	})

	ts, client := setupProwlarr(t, mux)
	defer ts.Close()

	statuses, err := client.IndexerStatuses()
	if err != nil {
		t.Fatalf("IndexerStatuses() failed: %v", err)
	}
	if len(statuses) != 1 || statuses[0].IndexerID != 1 {
		t.Errorf("unexpected statuses: %+v", statuses)
	}
}

func TestAddIndexer(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v1/indexer", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			t.Errorf("expected POST, got %s", r.Method)
		}
		w.Write([]byte(`{"id":10,"name":"NewIndexer","enable":true}`))
	})

	ts, client := setupProwlarr(t, mux)
	defer ts.Close()

	result, err := client.AddIndexer(map[string]interface{}{"name": "NewIndexer"})
	if err != nil {
		t.Fatalf("AddIndexer() failed: %v", err)
	}
	if result.ID != 10 || result.Name != "NewIndexer" {
		t.Errorf("unexpected result: %+v", result)
	}
}

func TestUpdateIndexer(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v1/indexer/5", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "PUT" {
			t.Errorf("expected PUT, got %s", r.Method)
		}
		w.Write([]byte(`{}`))
	})

	ts, client := setupProwlarr(t, mux)
	defer ts.Close()

	if err := client.UpdateIndexer(5, map[string]interface{}{"enable": true}); err != nil {
		t.Fatalf("UpdateIndexer() failed: %v", err)
	}
}

func TestDeleteIndexer(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v1/indexer/3", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "DELETE" {
			t.Errorf("expected DELETE, got %s", r.Method)
		}
		w.WriteHeader(200)
	})

	ts, client := setupProwlarr(t, mux)
	defer ts.Close()

	if err := client.DeleteIndexer(3); err != nil {
		t.Fatalf("DeleteIndexer() failed: %v", err)
	}
}

func TestTestAllIndexers(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v1/indexer/testall", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			t.Errorf("expected POST, got %s", r.Method)
		}
		json.NewEncoder(w).Encode([]IndexerTestResult{
			{ID: 1, IsValid: true},
			{ID: 2, IsValid: false, ValidationFailures: []struct {
				ErrorMessage string `json:"errorMessage"`
			}{{ErrorMessage: "connection refused"}}},
		})
	})

	ts, client := setupProwlarr(t, mux)
	defer ts.Close()

	results, err := client.TestAllIndexers()
	if err != nil {
		t.Fatalf("TestAllIndexers() failed: %v", err)
	}
	if len(results) != 2 {
		t.Fatalf("expected 2 results, got %d", len(results))
	}
	if results[0].IsValid != true || results[1].IsValid != false {
		t.Errorf("unexpected results: %+v", results)
	}
}

// --- Download Clients ---

func TestDownloadClients(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v3/downloadclient", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode([]DownloadClient{
			{
				ID:             1,
				Name:           "qBittorrent",
				Implementation: "QBittorrent",
				Enable:         true,
				Fields: []DownloadClientField{
					{Name: "host", Value: "gluetun"},
					{Name: "port", Value: 8080},
				},
			},
		})
	})

	ts, client := setupRadarr(t, mux)
	defer ts.Close()

	clients, err := client.DownloadClients()
	if err != nil {
		t.Fatalf("DownloadClients() failed: %v", err)
	}
	if len(clients) != 1 || clients[0].Implementation != "QBittorrent" {
		t.Errorf("unexpected clients: %+v", clients)
	}
	if clients[0].GetField("host") != "gluetun" {
		t.Errorf("expected host=gluetun, got %v", clients[0].GetField("host"))
	}
}

func TestGetMovieByID(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v3/movie/42", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]interface{}{
			"id": 42, "title": "Inception", "year": 2010,
		})
	})

	ts, client := setupRadarr(t, mux)
	defer ts.Close()

	movie, err := client.GetMovieByID(42)
	if err != nil {
		t.Fatalf("GetMovieByID() failed: %v", err)
	}
	if movie["title"] != "Inception" {
		t.Errorf("expected Inception, got %v", movie["title"])
	}
}

func TestUpdateMovie(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v3/movie/42", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "PUT" {
			t.Errorf("expected PUT, got %s", r.Method)
		}
		w.Write([]byte(`{}`))
	})

	ts, client := setupRadarr(t, mux)
	defer ts.Close()

	if err := client.UpdateMovie(42, map[string]interface{}{"qualityProfileId": 2}); err != nil {
		t.Fatalf("UpdateMovie() failed: %v", err)
	}
}

// --- Service/endpoint construction ---

func TestService(t *testing.T) {
	client := &Client{service: "radarr", ver: "v3"}
	if client.Service() != "radarr" {
		t.Errorf("expected radarr, got %s", client.Service())
	}
}

func TestEndpoint(t *testing.T) {
	client := &Client{ver: "v3"}
	if e := client.endpoint("movie"); e != "api/v3/movie" {
		t.Errorf("expected api/v3/movie, got %s", e)
	}

	client.ver = "v1"
	if e := client.endpoint("indexer"); e != "api/v1/indexer" {
		t.Errorf("expected api/v1/indexer, got %s", e)
	}
}

// --- Error handling ---

func TestMovies_ServerError(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v3/movie", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(500)
		w.Write([]byte(`Internal Server Error`))
	})

	ts, client := setupRadarr(t, mux)
	defer ts.Close()

	_, err := client.Movies()
	if err == nil {
		t.Error("expected error for 500 response")
	}
}

func TestMovies_EmptyResponse(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v3/movie", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode([]Movie{})
	})

	ts, client := setupRadarr(t, mux)
	defer ts.Close()

	movies, err := client.Movies()
	if err != nil {
		t.Fatalf("Movies() failed: %v", err)
	}
	if len(movies) != 0 {
		t.Errorf("expected 0 movies, got %d", len(movies))
	}
}

// --- Multi-endpoint test (real-world scenario) ---

func TestRadarrFullWorkflow(t *testing.T) {
	mux := http.NewServeMux()

	mux.HandleFunc("/api/v3/movie", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode([]Movie{
			{ID: 1, Title: "Inception", Year: 2010, HasFile: true},
		})
	})
	mux.HandleFunc("/api/v3/queue", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(QueuePage{TotalRecords: 0, Records: []QueueRecord{}})
	})
	mux.HandleFunc("/api/v3/health", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode([]HealthItem{})
	})
	mux.HandleFunc("/api/v3/rootfolder", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode([]RootFolder{
			{ID: 1, Path: "/data/media/movies", Accessible: true, FreeSpace: 500_000_000_000},
		})
	})
	mux.HandleFunc("/api/v3/qualityprofile", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode([]QualityProfile{
			{ID: 1, Name: "HD-1080p"},
		})
	})

	ts, client := setupRadarr(t, mux)
	defer ts.Close()

	movies, err := client.Movies()
	if err != nil {
		t.Fatalf("Movies: %v", err)
	}
	if len(movies) != 1 {
		t.Errorf("expected 1 movie, got %d", len(movies))
	}

	queue, err := client.Queue(50)
	if err != nil {
		t.Fatalf("Queue: %v", err)
	}
	if queue.TotalRecords != 0 {
		t.Errorf("expected 0 queued, got %d", queue.TotalRecords)
	}

	health, err := client.Health()
	if err != nil {
		t.Fatalf("Health: %v", err)
	}
	if len(health) != 0 {
		t.Errorf("expected 0 health issues, got %d", len(health))
	}

	folders, err := client.RootFolders()
	if err != nil {
		t.Fatalf("RootFolders: %v", err)
	}
	if len(folders) != 1 || folders[0].Path != "/data/media/movies" {
		t.Errorf("unexpected folders: %+v", folders)
	}

	profiles, err := client.QualityProfiles()
	if err != nil {
		t.Fatalf("QualityProfiles: %v", err)
	}
	if len(profiles) != 1 || profiles[0].Name != "HD-1080p" {
		t.Errorf("unexpected profiles: %+v", profiles)
	}
}
