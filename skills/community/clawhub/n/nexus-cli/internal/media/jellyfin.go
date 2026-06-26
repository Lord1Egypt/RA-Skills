package media

import (
	"fmt"

	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/keys"
)

// JellyfinServer implements MediaServer for Jellyfin.
type JellyfinServer struct{}

// Name returns the display name.
func (j *JellyfinServer) Name() string { return "Jellyfin" }

// RecentlyAdded returns the most recently added items from Jellyfin.
func (j *JellyfinServer) RecentlyAdded(limit int) ([]MediaItem, error) {
	// Get first user ID
	var users []struct {
		ID   string `json:"Id"`
		Name string `json:"Name"`
	}
	if err := api.GetJSON("jellyfin", "Users", nil, &users); err != nil || len(users) == 0 {
		return nil, fmt.Errorf("cannot get Jellyfin users")
	}
	userID := users[0].ID

	// Get latest items
	var items []struct {
		Name           string `json:"Name"`
		ProductionYear int    `json:"ProductionYear"`
		Type           string `json:"Type"`
		SeriesName     string `json:"SeriesName"`
	}
	params := map[string]string{
		"Limit":            fmt.Sprintf("%d", limit),
		"IncludeItemTypes": "Movie,Episode",
	}
	if err := api.GetJSON("jellyfin", fmt.Sprintf("Users/%s/Items/Latest", userID), params, &items); err != nil {
		return nil, err
	}

	var result []MediaItem
	for _, item := range items {
		year := fmt.Sprintf("%d", item.ProductionYear)
		if item.ProductionYear == 0 {
			year = "?"
		}
		label := item.Type
		name := item.Name
		if item.Type == "Episode" && item.SeriesName != "" {
			name = item.SeriesName + " — " + item.Name
			label = "Episode"
		}
		result = append(result, MediaItem{Title: name, Year: year, Type: label})
	}
	return result, nil
}

// LibraryScan triggers a full library refresh in Jellyfin.
func (j *JellyfinServer) LibraryScan() ([]ScanResult, error) {
	_, err := api.Post("jellyfin", "Library/Refresh", nil, nil)
	if err != nil {
		return []ScanResult{{Library: "All", OK: false, Err: err}}, err
	}
	return []ScanResult{{Library: "All", OK: true}}, nil
}

// WatchHistory returns watch history, using Tautulli if available, otherwise Jellyfin activity log.
func (j *JellyfinServer) WatchHistory(limit int) ([]WatchEntry, error) {
	// Try Tautulli first (optional companion service)
	key := keys.Get("tautulli")
	if key != "" && api.CheckReachable("tautulli") {
		return tautulliHistory(key, limit)
	}

	// Fall back to Jellyfin activity log
	var data struct {
		Items []struct {
			Name string `json:"Name"`
			Date string `json:"Date"`
		} `json:"Items"`
	}
	params := map[string]string{"Limit": fmt.Sprintf("%d", limit)}
	if err := api.GetJSON("jellyfin", "System/ActivityLog/Entries", params, &data); err != nil {
		return nil, err
	}

	var result []WatchEntry
	for _, item := range data.Items {
		result = append(result, WatchEntry{
			Title: item.Name,
			User:  "",
		})
	}
	return result, nil
}

// tautulliHistory fetches watch history from Tautulli.
func tautulliHistory(apiKey string, limit int) ([]WatchEntry, error) {
	var data struct {
		Response struct {
			Data struct {
				Data []struct {
					FullTitle string `json:"full_title"`
					User      string `json:"user"`
					Duration  int    `json:"duration"`
				} `json:"data"`
			} `json:"data"`
		} `json:"response"`
	}
	params := map[string]string{
		"apikey": apiKey,
		"cmd":    "get_history",
		"length": fmt.Sprintf("%d", limit),
	}
	if err := api.GetJSON("tautulli", "api/v2", params, &data); err != nil {
		return nil, err
	}

	var result []WatchEntry
	for _, h := range data.Response.Data.Data {
		result = append(result, WatchEntry{
			Title:   h.FullTitle,
			User:    h.User,
			Minutes: h.Duration / 60,
		})
	}
	return result, nil
}
