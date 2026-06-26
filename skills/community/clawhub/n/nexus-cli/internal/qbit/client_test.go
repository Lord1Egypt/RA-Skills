package qbit

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/maxtechera/admirarr/internal/config"
	"github.com/spf13/viper"
)

func setupQbit(t *testing.T, handler http.Handler) (*httptest.Server, *Client) {
	t.Helper()
	ts := httptest.NewServer(handler)
	addr := strings.TrimPrefix(ts.URL, "http://")
	parts := strings.SplitN(addr, ":", 2)
	var port int
	fmt.Sscanf(parts[1], "%d", &port)
	viper.Set("services.qbittorrent.host", parts[0])
	viper.Set("services.qbittorrent.port", port)
	config.Load()
	return ts, New()
}

func TestTorrents(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v2/torrents/info", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode([]Torrent{
			{Hash: "abc123", Name: "Inception.2010.1080p", Size: 5_000_000_000, Progress: 0.75, DLSpeed: 10_000_000, State: "downloading", ETA: 300, Category: "movies"},
			{Hash: "def456", Name: "The.Matrix.1999", Size: 3_000_000_000, Progress: 1.0, DLSpeed: 0, State: "uploading", Category: "movies"},
		})
	})

	ts, client := setupQbit(t, mux)
	defer ts.Close()

	torrents, err := client.Torrents()
	if err != nil {
		t.Fatalf("Torrents() failed: %v", err)
	}
	if len(torrents) != 2 {
		t.Fatalf("expected 2 torrents, got %d", len(torrents))
	}
	if torrents[0].Name != "Inception.2010.1080p" {
		t.Errorf("unexpected name: %s", torrents[0].Name)
	}
	if torrents[0].Progress != 0.75 {
		t.Errorf("expected progress=0.75, got %f", torrents[0].Progress)
	}
	if torrents[1].State != "uploading" {
		t.Errorf("expected state=uploading, got %s", torrents[1].State)
	}
}

func TestTorrents_Empty(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v2/torrents/info", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode([]Torrent{})
	})

	ts, client := setupQbit(t, mux)
	defer ts.Close()

	torrents, err := client.Torrents()
	if err != nil {
		t.Fatalf("Torrents() failed: %v", err)
	}
	if len(torrents) != 0 {
		t.Errorf("expected 0 torrents, got %d", len(torrents))
	}
}

func TestPreferences(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v2/app/preferences", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(Preferences{
			SavePath:     "/data/torrents",
			WebUIPort:    8080,
			ListenPort:   6881,
			DLLimit:      0,
			UPLimit:      100000,
			WebUIAddress: "*",
		})
	})

	ts, client := setupQbit(t, mux)
	defer ts.Close()

	prefs, err := client.Preferences()
	if err != nil {
		t.Fatalf("Preferences() failed: %v", err)
	}
	if prefs.SavePath != "/data/torrents" {
		t.Errorf("expected save_path=/data/torrents, got %s", prefs.SavePath)
	}
	if prefs.ListenPort != 6881 {
		t.Errorf("expected listen_port=6881, got %d", prefs.ListenPort)
	}
}

func TestVersion(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v2/app/version", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("v4.6.3\n"))
	})

	ts, client := setupQbit(t, mux)
	defer ts.Close()

	ver, err := client.Version()
	if err != nil {
		t.Fatalf("Version() failed: %v", err)
	}
	if ver != "v4.6.3" {
		t.Errorf("expected v4.6.3, got %q", ver)
	}
}

func TestCategories(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v2/torrents/categories", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]Category{
			"movies":    {Name: "movies", SavePath: "/data/torrents/movies"},
			"tv-sonarr": {Name: "tv-sonarr", SavePath: "/data/torrents/tv"},
		})
	})

	ts, client := setupQbit(t, mux)
	defer ts.Close()

	cats, err := client.Categories()
	if err != nil {
		t.Fatalf("Categories() failed: %v", err)
	}
	if len(cats) != 2 {
		t.Fatalf("expected 2 categories, got %d", len(cats))
	}
	if cats["movies"].SavePath != "/data/torrents/movies" {
		t.Errorf("unexpected movies save path: %s", cats["movies"].SavePath)
	}
}

func TestPause(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v2/torrents/pause", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			t.Errorf("expected POST, got %s", r.Method)
		}
		r.ParseForm()
		if r.FormValue("hashes") != "abc123|def456" {
			t.Errorf("expected hashes=abc123|def456, got %s", r.FormValue("hashes"))
		}
		w.WriteHeader(200)
	})

	ts, client := setupQbit(t, mux)
	defer ts.Close()

	if err := client.Pause("abc123", "def456"); err != nil {
		t.Fatalf("Pause() failed: %v", err)
	}
}

func TestResume(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v2/torrents/resume", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			t.Errorf("expected POST, got %s", r.Method)
		}
		r.ParseForm()
		if r.FormValue("hashes") != "all" {
			t.Errorf("expected hashes=all, got %s", r.FormValue("hashes"))
		}
		w.WriteHeader(200)
	})

	ts, client := setupQbit(t, mux)
	defer ts.Close()

	if err := client.Resume("all"); err != nil {
		t.Fatalf("Resume() failed: %v", err)
	}
}

func TestDelete(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v2/torrents/delete", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			t.Errorf("expected POST, got %s", r.Method)
		}
		r.ParseForm()
		if r.FormValue("hashes") != "abc123" {
			t.Errorf("expected hashes=abc123, got %s", r.FormValue("hashes"))
		}
		if r.FormValue("deleteFiles") != "true" {
			t.Errorf("expected deleteFiles=true, got %s", r.FormValue("deleteFiles"))
		}
		w.WriteHeader(200)
	})

	ts, client := setupQbit(t, mux)
	defer ts.Close()

	if err := client.Delete(true, "abc123"); err != nil {
		t.Fatalf("Delete() failed: %v", err)
	}
}

func TestDelete_NoFiles(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v2/torrents/delete", func(w http.ResponseWriter, r *http.Request) {
		r.ParseForm()
		if r.FormValue("deleteFiles") != "false" {
			t.Errorf("expected deleteFiles=false, got %s", r.FormValue("deleteFiles"))
		}
		w.WriteHeader(200)
	})

	ts, client := setupQbit(t, mux)
	defer ts.Close()

	if err := client.Delete(false, "abc123"); err != nil {
		t.Fatalf("Delete(false) failed: %v", err)
	}
}

// --- Multi-endpoint workflow ---

func TestQbitFullWorkflow(t *testing.T) {
	mux := http.NewServeMux()

	mux.HandleFunc("/api/v2/torrents/info", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode([]Torrent{
			{Hash: "abc", Name: "Movie.torrent", Progress: 0.5, State: "downloading"},
		})
	})
	mux.HandleFunc("/api/v2/app/version", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("v4.6.3"))
	})
	mux.HandleFunc("/api/v2/app/preferences", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(Preferences{SavePath: "/data/torrents"})
	})
	mux.HandleFunc("/api/v2/torrents/categories", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]Category{
			"movies": {Name: "movies", SavePath: "/data/torrents/movies"},
		})
	})

	ts, client := setupQbit(t, mux)
	defer ts.Close()

	torrents, err := client.Torrents()
	if err != nil {
		t.Fatalf("Torrents: %v", err)
	}
	if len(torrents) != 1 {
		t.Errorf("expected 1 torrent, got %d", len(torrents))
	}

	ver, err := client.Version()
	if err != nil {
		t.Fatalf("Version: %v", err)
	}
	if ver != "v4.6.3" {
		t.Errorf("expected v4.6.3, got %s", ver)
	}

	prefs, err := client.Preferences()
	if err != nil {
		t.Fatalf("Preferences: %v", err)
	}
	if prefs.SavePath != "/data/torrents" {
		t.Errorf("expected /data/torrents, got %s", prefs.SavePath)
	}

	cats, err := client.Categories()
	if err != nil {
		t.Fatalf("Categories: %v", err)
	}
	if len(cats) != 1 {
		t.Errorf("expected 1 category, got %d", len(cats))
	}
}
