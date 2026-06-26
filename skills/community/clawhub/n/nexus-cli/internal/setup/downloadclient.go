package setup

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/ui"
)

// arrDownloadConfig maps *Arr services to their qBittorrent category settings.
var arrDownloadConfig = []struct {
	Service       string
	Category      string
	CategoryField string
	TorrentDir    string
}{
	{"radarr", "movies", "movieCategory", "torrents/movies"},
	{"sonarr", "tv-sonarr", "tvCategory", "torrents/tv"},
	{"lidarr", "music", "musicCategory", "torrents/music"},
	{"readarr", "books", "bookCategory", "torrents/books"},
	{"whisparr", "xxx", "movieCategory", "torrents/xxx"},
}

// ConfigureDownloadClients runs Phase 5: download client + qBittorrent configuration.
func ConfigureDownloadClients(state *SetupState) StepResult {
	r := StepResult{Name: "Download Clients"}

	// 5a. Check/fix download clients in all reachable *Arr services
	for _, dc := range arrDownloadConfig {
		svc := state.Services[dc.Service]
		if svc == nil || !svc.Reachable {
			if hasService(state, dc.Service) {
				fmt.Printf("  %s %-15s %s\n", ui.Dim("—"), dc.Service, ui.Dim("skipped (not reachable)"))
				r.skip()
			}
			continue
		}
		checkArrDownloadClient(state, &r, dc.Service, dc.Category)
	}

	// 5b. Fix qBittorrent categories
	if svc := state.Services["qbittorrent"]; svc != nil && svc.Reachable {
		checkQbitCategories(state, &r)
		// 5c. Verify default save path
		checkQbitDefaultPath(state, &r)
	} else {
		fmt.Printf("  %s %-15s %s\n", ui.Dim("—"), "qbittorrent", ui.Dim("skipped (not reachable)"))
		r.skip()
	}

	// 5d. Create missing download directories
	checkDownloadDirs(state, &r)

	return r
}

func checkArrDownloadClient(state *SetupState, r *StepResult, service, expectedCategory string) {
	client := arr.New(service)

	clients, err := client.DownloadClients()
	if err != nil {
		r.errf("%s: cannot query download clients: %v", service, err)
		return
	}

	// Find qBittorrent client
	var qbitClient *arr.DownloadClient
	for i := range clients {
		if clients[i].Implementation == "QBittorrent" {
			qbitClient = &clients[i]
			break
		}
	}

	if qbitClient == nil {
		fmt.Printf("  %s %s → No qBittorrent client — creating\n", ui.GoldText("↻"), titleCase(service))
		if createQbitClient(state, r, service, expectedCategory) {
			r.fix()
		}
		return
	}

	// Validate existing client settings
	host := fmt.Sprintf("%v", qbitClient.GetField("host"))
	port := qbitClient.GetField("port")
	var category string
	categoryField := categoryFieldFor(service)
	if v := qbitClient.GetField(categoryField); v != nil {
		category = fmt.Sprintf("%v", v)
	}

	expectedHost := "gluetun"
	issues := []string{}
	if host != expectedHost && host != "localhost" && host != "127.0.0.1" && host != "qbittorrent" {
		issues = append(issues, fmt.Sprintf("host=%s (should be %s)", host, expectedHost))
	}
	if fmt.Sprintf("%v", port) != "8080" {
		issues = append(issues, fmt.Sprintf("port=%v (expected 8080)", port))
	}
	if category != expectedCategory {
		issues = append(issues, fmt.Sprintf("category=%s (should be %s)", category, expectedCategory))
	}

	if len(issues) == 0 {
		fmt.Printf("  %s %s → qBittorrent client OK (host=%s, category=%s)\n",
			ui.Ok("✓"), titleCase(service), host, category)
		r.pass()
		return
	}

	// Auto-fix
	fmt.Printf("  %s %s → Fixing: %s\n", ui.GoldText("↻"), titleCase(service), strings.Join(issues, ", "))

	qbitClient.SetField("host", expectedHost)
	qbitClient.SetField("port", 8080)
	qbitClient.SetField(categoryField, expectedCategory)

	if err := client.UpdateDownloadClient(qbitClient); err != nil {
		r.errf("%s: failed to update download client: %v", service, err)
		return
	}

	fmt.Printf("  %s %s → Download client fixed\n", ui.Ok("✓"), titleCase(service))
	r.fix()
}

func createQbitClient(state *SetupState, r *StepResult, service, category string) bool {
	client := arr.New(service)

	// Get schema for QBittorrent implementation
	schemas, err := client.DownloadClientSchemas()
	if err != nil {
		r.errf("%s: cannot get download client schema: %v", service, err)
		return false
	}

	var schema *arr.DownloadClient
	for i := range schemas {
		if schemas[i].Implementation == "QBittorrent" {
			schema = &schemas[i]
			break
		}
	}
	if schema == nil {
		r.errf("%s: QBittorrent schema not found", service)
		return false
	}

	// Configure the client — use gluetun as host (qBit uses Gluetun's network)
	schema.Name = "qBittorrent"
	schema.Enable = true
	schema.Priority = 1
	schema.RemoveCompletedDownloads = true
	schema.RemoveFailedDownloads = true
	schema.SetField("host", "gluetun")
	schema.SetField("port", 8080)
	schema.SetField("username", "admin")
	schema.SetField("password", "") // default on fresh install

	schema.SetField(categoryFieldFor(service), category)

	if err := client.CreateDownloadClient(schema); err != nil {
		r.errf("%s: failed to create download client: %v", service, err)
		return false
	}

	fmt.Printf("  %s %s → qBittorrent download client created\n", ui.Ok("✓"), titleCase(service))
	return true
}

func checkQbitCategories(state *SetupState, r *StepResult) {
	fmt.Printf("\n  %s\n", ui.Bold("  qBittorrent Categories"))

	dataPath := state.DataPath
	if dataPath == "" {
		dataPath = config.DataPath()
	}

	// Build categories from active *Arr services
	expectedCategories := map[string]string{}
	for _, dc := range arrDownloadConfig {
		svc := state.Services[dc.Service]
		if svc != nil && svc.Reachable {
			expectedCategories[dc.Category] = dataPath + "/" + dc.TorrentDir
		}
	}

	// Fix via qBittorrent API
	qbitURL := config.ServiceURL("qbittorrent")

	for catName, expectedPath := range expectedCategories {
		c := &http.Client{Timeout: 5 * time.Second}
		resp, err := c.Get(qbitURL + "/api/v2/torrents/categories")
		if err != nil {
			r.errf("cannot query qBittorrent categories: %v", err)
			return
		}
		body, _ := io.ReadAll(resp.Body)
		resp.Body.Close()

		var categories map[string]struct {
			SavePath string `json:"savePath"`
		}
		if err := json.Unmarshal(body, &categories); err != nil {
			r.errf("cannot parse qBittorrent categories: %v", err)
			return
		}

		cat, exists := categories[catName]
		if exists && cat.SavePath == expectedPath {
			fmt.Printf("  %s %s → %s\n", ui.Ok("✓"), catName, expectedPath)
			r.pass()
			continue
		}

		current := "(not set)"
		if exists {
			current = cat.SavePath
		}
		fmt.Printf("  %s %s → %s (expected %s) — fixing\n", ui.GoldText("↻"), catName, current, expectedPath)

		params := url.Values{}
		params.Set("category", catName)
		params.Set("savePath", expectedPath)

		var apiEndpoint string
		if exists {
			apiEndpoint = "/api/v2/torrents/editCategory"
		} else {
			apiEndpoint = "/api/v2/torrents/createCategory"
		}

		req, _ := http.NewRequest("POST", qbitURL+apiEndpoint, strings.NewReader(params.Encode()))
		req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
		resp2, err := c.Do(req)
		if err != nil {
			r.errf("failed to fix qBittorrent category %s via API: %v", catName, err)
			continue
		}
		resp2.Body.Close()

		fmt.Printf("  %s %s → %s (fixed)\n", ui.Ok("✓"), catName, expectedPath)
		r.fix()
	}
}

func checkQbitDefaultPath(state *SetupState, r *StepResult) {
	fmt.Printf("\n  %s\n", ui.Bold("  qBittorrent Default Save Path"))

	qbitURL := config.ServiceURL("qbittorrent")
	c := &http.Client{Timeout: 5 * time.Second}
	resp, err := c.Get(qbitURL + "/api/v2/app/preferences")
	if err != nil {
		r.errf("cannot query qBittorrent preferences: %v", err)
		return
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)

	var prefs struct {
		SavePath string `json:"save_path"`
	}
	if err := json.Unmarshal(body, &prefs); err != nil {
		r.errf("cannot parse qBittorrent preferences: %v", err)
		return
	}

	dataPath := state.DataPath
	if dataPath == "" {
		dataPath = config.DataPath()
	}
	expectedPath := dataPath + "/torrents"

	if prefs.SavePath == expectedPath {
		fmt.Printf("  %s Default save path: %s\n", ui.Ok("✓"), prefs.SavePath)
		r.pass()
		return
	}

	fmt.Printf("  %s Default save path: %s (expected %s) — fixing\n", ui.GoldText("↻"), prefs.SavePath, expectedPath)

	payload := fmt.Sprintf(`json={"save_path":"%s"}`, expectedPath)
	req, _ := http.NewRequest("POST", qbitURL+"/api/v2/app/setPreferences",
		strings.NewReader(payload))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	resp2, err := c.Do(req)
	if err != nil {
		r.errf("failed to fix qBittorrent save path: %v", err)
		return
	}
	resp2.Body.Close()

	fmt.Printf("  %s Default save path fixed to %s\n", ui.Ok("✓"), expectedPath)
	r.fix()
}

// titleCase capitalises the first letter of a service name (e.g. "radarr" → "Radarr").
func titleCase(s string) string {
	if s == "" {
		return s
	}
	return strings.ToUpper(s[:1]) + s[1:]
}

// categoryFieldFor returns the correct *Arr download client category field name
// by looking it up in arrDownloadConfig.
func categoryFieldFor(service string) string {
	for _, dc := range arrDownloadConfig {
		if dc.Service == service {
			return dc.CategoryField
		}
	}
	return "movieCategory" // fallback
}

func checkDownloadDirs(state *SetupState, r *StepResult) {
	dataPath := state.DataPath
	if dataPath == "" {
		dataPath = config.DataPath()
	}

	dirs := []string{
		filepath.Join(dataPath, "torrents"),
		filepath.Join(dataPath, "torrents", "movies"),
		filepath.Join(dataPath, "torrents", "tv"),
	}

	for _, dir := range dirs {
		if info, err := os.Stat(dir); err == nil && info.IsDir() {
			r.pass()
			continue
		}
		if err := os.MkdirAll(dir, 0755); err != nil {
			r.errf("cannot create %s: %v", dir, err)
			continue
		}
		fmt.Printf("  %s Created %s\n", ui.Ok("✓"), dir)
		r.fix()
	}
}
