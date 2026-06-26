package seerr

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

func setupSeerr(t *testing.T, handler http.Handler) (*httptest.Server, *Client) {
	t.Helper()
	ts := httptest.NewServer(handler)
	addr := strings.TrimPrefix(ts.URL, "http://")
	parts := strings.SplitN(addr, ":", 2)
	var port int
	fmt.Sscanf(parts[1], "%d", &port)
	viper.Set("services.seerr.host", parts[0])
	viper.Set("services.seerr.port", port)
	config.Load()
	return ts, New()
}

func TestRequests(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v1/request", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Query().Get("take") != "20" {
			t.Errorf("expected take=20, got %s", r.URL.Query().Get("take"))
		}
		if r.URL.Query().Get("sort") != "added" {
			t.Errorf("expected sort=added, got %s", r.URL.Query().Get("sort"))
		}
		json.NewEncoder(w).Encode(RequestPage{
			PageInfo: struct {
				Results int `json:"results"`
			}{Results: 2},
			Results: []Request{
				{
					ID:     1,
					Status: 2,
					Type:   "movie",
					Media: struct {
						MediaType string `json:"mediaType"`
						TmdbID    int    `json:"tmdbId"`
					}{MediaType: "movie", TmdbID: 27205},
					RequestedBy: struct {
						DisplayName string `json:"displayName"`
					}{DisplayName: "Max"},
				},
				{
					ID:     2,
					Status: 1,
					Type:   "tv",
					Is4K:   true,
					Media: struct {
						MediaType string `json:"mediaType"`
						TmdbID    int    `json:"tmdbId"`
					}{MediaType: "tv", TmdbID: 1396},
					RequestedBy: struct {
						DisplayName string `json:"displayName"`
					}{DisplayName: "Alice"},
				},
			},
		})
	})

	ts, client := setupSeerr(t, mux)
	defer ts.Close()

	page, err := client.Requests(20)
	if err != nil {
		t.Fatalf("Requests() failed: %v", err)
	}
	if page.PageInfo.Results != 2 {
		t.Errorf("expected 2 results, got %d", page.PageInfo.Results)
	}
	if len(page.Results) != 2 {
		t.Fatalf("expected 2 requests, got %d", len(page.Results))
	}
	if page.Results[0].Media.TmdbID != 27205 {
		t.Errorf("expected tmdbId=27205, got %d", page.Results[0].Media.TmdbID)
	}
	if page.Results[1].Is4K != true {
		t.Error("expected request[1] is4K=true")
	}
	if page.Results[1].RequestedBy.DisplayName != "Alice" {
		t.Errorf("expected Alice, got %s", page.Results[1].RequestedBy.DisplayName)
	}
}

func TestRequests_Empty(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v1/request", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(RequestPage{
			PageInfo: struct {
				Results int `json:"results"`
			}{Results: 0},
			Results: []Request{},
		})
	})

	ts, client := setupSeerr(t, mux)
	defer ts.Close()

	page, err := client.Requests(10)
	if err != nil {
		t.Fatalf("Requests() failed: %v", err)
	}
	if len(page.Results) != 0 {
		t.Errorf("expected 0 requests, got %d", len(page.Results))
	}
}

func TestResolveTitle_Movie(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v1/movie/27205", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]interface{}{
			"title":       "Inception",
			"releaseDate": "2010-07-16",
		})
	})

	ts, client := setupSeerr(t, mux)
	defer ts.Close()

	title, year := client.ResolveTitle("movie", 27205)
	if title != "Inception" {
		t.Errorf("expected Inception, got %s", title)
	}
	if year != "2010" {
		t.Errorf("expected 2010, got %s", year)
	}
}

func TestResolveTitle_TV(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v1/tv/1396", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]interface{}{
			"name":         "Breaking Bad",
			"firstAirDate": "2008-01-20",
		})
	})

	ts, client := setupSeerr(t, mux)
	defer ts.Close()

	title, year := client.ResolveTitle("tv", 1396)
	if title != "Breaking Bad" {
		t.Errorf("expected Breaking Bad, got %s", title)
	}
	if year != "2008" {
		t.Errorf("expected 2008, got %s", year)
	}
}

func TestResolveTitle_Fallback(t *testing.T) {
	mux := http.NewServeMux()
	// No handler — 404 triggers fallback

	ts, client := setupSeerr(t, mux)
	defer ts.Close()

	title, year := client.ResolveTitle("movie", 99999)
	if title != "TMDB:99999" {
		t.Errorf("expected fallback title, got %s", title)
	}
	if year != "?" {
		t.Errorf("expected ?, got %s", year)
	}
}

func TestResolveTitle_MissingFields(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/v1/movie/12345", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]interface{}{
			"id": 12345,
			// no title, no releaseDate
		})
	})

	ts, client := setupSeerr(t, mux)
	defer ts.Close()

	title, year := client.ResolveTitle("movie", 12345)
	if title != "?" {
		t.Errorf("expected ?, got %s", title)
	}
	if year != "?" {
		t.Errorf("expected ?, got %s", year)
	}
}

// --- Full workflow ---

func TestSeerrFullWorkflow(t *testing.T) {
	mux := http.NewServeMux()

	mux.HandleFunc("/api/v1/request", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(RequestPage{
			PageInfo: struct {
				Results int `json:"results"`
			}{Results: 1},
			Results: []Request{
				{
					ID:     1,
					Status: 2,
					Type:   "movie",
					Media: struct {
						MediaType string `json:"mediaType"`
						TmdbID    int    `json:"tmdbId"`
					}{MediaType: "movie", TmdbID: 27205},
				},
			},
		})
	})

	mux.HandleFunc("/api/v1/movie/27205", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]interface{}{
			"title":       "Inception",
			"releaseDate": "2010-07-16",
		})
	})

	ts, client := setupSeerr(t, mux)
	defer ts.Close()

	// Fetch requests
	page, err := client.Requests(20)
	if err != nil {
		t.Fatalf("Requests: %v", err)
	}
	if len(page.Results) != 1 {
		t.Fatalf("expected 1 request, got %d", len(page.Results))
	}

	// Resolve title for the request
	req := page.Results[0]
	title, year := client.ResolveTitle(req.Media.MediaType, req.Media.TmdbID)
	if title != "Inception" || year != "2010" {
		t.Errorf("expected Inception (2010), got %s (%s)", title, year)
	}
}
