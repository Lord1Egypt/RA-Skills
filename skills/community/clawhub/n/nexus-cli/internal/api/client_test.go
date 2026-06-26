package api

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

func TestGet_Success(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "GET" {
			t.Errorf("expected GET, got %s", r.Method)
		}
		w.Write([]byte(`{"status":"ok"}`))
	}))
	defer ts.Close()

	addr := strings.TrimPrefix(ts.URL, "http://")
	parts := strings.SplitN(addr, ":", 2)
	var port int
	fmt.Sscanf(parts[1], "%d", &port)

	viper.Set("services.testget.host", parts[0])
	viper.Set("services.testget.port", port)
	config.Load()

	data, err := Get("testget", "", nil)
	if err != nil {
		t.Fatalf("Get failed: %v", err)
	}
	if string(data) != `{"status":"ok"}` {
		t.Errorf("unexpected body: %s", data)
	}
}

func TestGetJSON_Unmarshal(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{"name": "radarr", "version": "5.0"})
	}))
	defer ts.Close()

	addr := strings.TrimPrefix(ts.URL, "http://")
	parts := strings.SplitN(addr, ":", 2)
	var port int
	fmt.Sscanf(parts[1], "%d", &port)
	viper.Set("services.testjson.host", parts[0])
	viper.Set("services.testjson.port", port)
	config.Load()

	var target struct {
		Name    string `json:"name"`
		Version string `json:"version"`
	}
	if err := GetJSON("testjson", "", nil, &target); err != nil {
		t.Fatalf("GetJSON failed: %v", err)
	}
	if target.Name != "radarr" {
		t.Errorf("expected name=radarr, got %s", target.Name)
	}
	if target.Version != "5.0" {
		t.Errorf("expected version=5.0, got %s", target.Version)
	}
}

func TestPost_SendsJSON(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			t.Errorf("expected POST, got %s", r.Method)
		}
		if ct := r.Header.Get("Content-Type"); ct != "application/json" {
			t.Errorf("expected application/json, got %s", ct)
		}
		body, _ := io.ReadAll(r.Body)
		var payload map[string]string
		json.Unmarshal(body, &payload)
		if payload["path"] != "/movies" {
			t.Errorf("expected path=/movies, got %s", payload["path"])
		}
		w.Write([]byte(`{"id":1}`))
	}))
	defer ts.Close()

	addr := strings.TrimPrefix(ts.URL, "http://")
	parts := strings.SplitN(addr, ":", 2)
	var port int
	fmt.Sscanf(parts[1], "%d", &port)
	viper.Set("services.testpost.host", parts[0])
	viper.Set("services.testpost.port", port)
	config.Load()

	data, err := Post("testpost", "api/v3/rootfolder", map[string]string{"path": "/movies"}, nil)
	if err != nil {
		t.Fatalf("Post failed: %v", err)
	}
	if !strings.Contains(string(data), `"id":1`) {
		t.Errorf("unexpected response: %s", data)
	}
}

func TestPut_SendsJSON(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "PUT" {
			t.Errorf("expected PUT, got %s", r.Method)
		}
		if ct := r.Header.Get("Content-Type"); ct != "application/json" {
			t.Errorf("expected application/json, got %s", ct)
		}
		body, _ := io.ReadAll(r.Body)
		w.Write(body) // Echo back
	}))
	defer ts.Close()

	addr := strings.TrimPrefix(ts.URL, "http://")
	parts := strings.SplitN(addr, ":", 2)
	var port int
	fmt.Sscanf(parts[1], "%d", &port)
	viper.Set("services.testput.host", parts[0])
	viper.Set("services.testput.port", port)
	config.Load()

	payload := map[string]interface{}{"id": 1, "host": "localhost"}
	data, err := Put("testput", "api/v3/downloadclient/1", payload, nil)
	if err != nil {
		t.Fatalf("Put failed: %v", err)
	}
	var result map[string]interface{}
	json.Unmarshal(data, &result)
	if result["host"] != "localhost" {
		t.Errorf("expected host=localhost, got %v", result["host"])
	}
}

func TestPostJSON_Unmarshal(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"id":42,"name":"test"}`))
	}))
	defer ts.Close()

	addr := strings.TrimPrefix(ts.URL, "http://")
	parts := strings.SplitN(addr, ":", 2)
	var port int
	fmt.Sscanf(parts[1], "%d", &port)
	viper.Set("services.testpostjson.host", parts[0])
	viper.Set("services.testpostjson.port", port)
	config.Load()

	var target struct {
		ID   int    `json:"id"`
		Name string `json:"name"`
	}
	err := PostJSON("testpostjson", "api/test", map[string]string{"key": "val"}, nil, &target)
	if err != nil {
		t.Fatalf("PostJSON failed: %v", err)
	}
	if target.ID != 42 || target.Name != "test" {
		t.Errorf("unexpected result: %+v", target)
	}
}

func TestPutJSON_Unmarshal(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"id":1,"updated":true}`))
	}))
	defer ts.Close()

	addr := strings.TrimPrefix(ts.URL, "http://")
	parts := strings.SplitN(addr, ":", 2)
	var port int
	fmt.Sscanf(parts[1], "%d", &port)
	viper.Set("services.testputjson.host", parts[0])
	viper.Set("services.testputjson.port", port)
	config.Load()

	var target struct {
		ID      int  `json:"id"`
		Updated bool `json:"updated"`
	}
	err := PutJSON("testputjson", "api/test", map[string]string{"field": "value"}, nil, &target)
	if err != nil {
		t.Fatalf("PutJSON failed: %v", err)
	}
	if !target.Updated {
		t.Error("expected updated=true")
	}
}

func TestCheckReachable_Up(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(200)
	}))
	defer ts.Close()

	addr := strings.TrimPrefix(ts.URL, "http://")
	parts := strings.SplitN(addr, ":", 2)
	var port int
	fmt.Sscanf(parts[1], "%d", &port)
	viper.Set("services.qbittorrent.host", parts[0])
	viper.Set("services.qbittorrent.port", port)
	config.Load()

	if !CheckReachable("qbittorrent") {
		t.Error("expected qbittorrent to be reachable")
	}
}

func TestCheckReachable_Down(t *testing.T) {
	// Point to a port that nothing listens on
	viper.Set("services.qbittorrent.host", "127.0.0.1")
	viper.Set("services.qbittorrent.port", 1) // unlikely to be open
	config.Load()

	if CheckReachable("qbittorrent") {
		t.Error("expected qbittorrent to be unreachable")
	}
}

func TestGet_WithParams(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Query().Get("pageSize") != "10" {
			t.Errorf("expected pageSize=10, got %s", r.URL.Query().Get("pageSize"))
		}
		w.Write([]byte(`{"ok":true}`))
	}))
	defer ts.Close()

	addr := strings.TrimPrefix(ts.URL, "http://")
	parts := strings.SplitN(addr, ":", 2)
	var port int
	fmt.Sscanf(parts[1], "%d", &port)
	viper.Set("services.testparams.host", parts[0])
	viper.Set("services.testparams.port", port)
	config.Load()

	_, err := Get("testparams", "api/v3/queue", map[string]string{"pageSize": "10"})
	if err != nil {
		t.Fatalf("Get with params failed: %v", err)
	}
}

func TestGet_ConnectionRefused(t *testing.T) {
	viper.Set("services.deadservice.host", "127.0.0.1")
	viper.Set("services.deadservice.port", 1)
	config.Load()

	_, err := Get("deadservice", "api/test", nil)
	if err == nil {
		t.Error("expected error for connection refused")
	}
}

func TestBuildURL_APIKeyInjection(t *testing.T) {
	// Sonarr should get apikey as query param
	viper.Set("services.sonarr.host", "localhost")
	viper.Set("services.sonarr.port", 8989)
	viper.Set("keys.sonarr", "test-key-123")
	config.Load()

	url := buildURL("sonarr", "api/v3/health", nil)
	if !strings.Contains(url, "apikey=test-key-123") {
		t.Errorf("expected apikey in URL, got: %s", url)
	}
	if !strings.Contains(url, "localhost:8989") {
		t.Errorf("expected localhost:8989 in URL, got: %s", url)
	}
}

func TestAddAuth_SeerrHeader(t *testing.T) {
	viper.Set("keys.seerr", "seerr-key-456")
	config.Load()

	req, _ := http.NewRequest("GET", "http://localhost/api/v1/status", nil)
	addAuth(req, "seerr")

	if got := req.Header.Get("X-Api-Key"); got != "seerr-key-456" {
		t.Errorf("expected X-Api-Key=seerr-key-456, got %s", got)
	}
}
