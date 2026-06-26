package media

import (
	"encoding/xml"
	"fmt"

	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/keys"
)

// PlexServer implements MediaServer for Plex + Tautulli.
type PlexServer struct{}

// Name returns the display name.
func (p *PlexServer) Name() string { return "Plex" }

// RecentlyAdded returns the most recently added items from Plex.
func (p *PlexServer) RecentlyAdded(limit int) ([]MediaItem, error) {
	params := map[string]string{
		"X-Plex-Token": keys.Get("plex"),
	}
	body, err := api.Get("plex", "library/recentlyAdded", params)
	if err != nil {
		return nil, err
	}

	var container struct {
		XMLName xml.Name `xml:"MediaContainer"`
		Videos  []struct {
			Title           string `xml:"title,attr"`
			Year            string `xml:"year,attr"`
			Type            string `xml:"type,attr"`
			GrandparentTitle string `xml:"grandparentTitle,attr"`
		} `xml:"Video"`
	}
	if err := xml.Unmarshal(body, &container); err != nil {
		return nil, fmt.Errorf("parse Plex XML: %w", err)
	}

	var result []MediaItem
	for i, v := range container.Videos {
		if i >= limit {
			break
		}
		label := v.Type
		name := v.Title
		if v.Type == "episode" && v.GrandparentTitle != "" {
			name = v.GrandparentTitle + " — " + v.Title
			label = "Episode"
		} else if v.Type == "movie" {
			label = "Movie"
		}
		year := v.Year
		if year == "" {
			year = "?"
		}
		result = append(result, MediaItem{Title: name, Year: year, Type: label})
	}
	return result, nil
}

// LibraryScan triggers a scan on all Plex library sections.
func (p *PlexServer) LibraryScan() ([]ScanResult, error) {
	// Get all library sections
	var sections struct {
		XMLName xml.Name `xml:"MediaContainer"`
		Dirs    []struct {
			Key   string `xml:"key,attr"`
			Title string `xml:"title,attr"`
		} `xml:"Directory"`
	}
	body, err := api.Get("plex", "library/sections", map[string]string{
		"X-Plex-Token": keys.Get("plex"),
	})
	if err != nil {
		return nil, fmt.Errorf("get Plex sections: %w", err)
	}
	if err := xml.Unmarshal(body, &sections); err != nil {
		return nil, fmt.Errorf("parse Plex sections: %w", err)
	}

	var results []ScanResult
	for _, dir := range sections.Dirs {
		endpoint := fmt.Sprintf("library/sections/%s/refresh", dir.Key)
		_, err := api.Post("plex", endpoint, nil, map[string]string{
			"X-Plex-Token": keys.Get("plex"),
		})
		if err != nil {
			results = append(results, ScanResult{Library: dir.Title, OK: false, Err: err})
		} else {
			results = append(results, ScanResult{Library: dir.Title, OK: true})
		}
	}
	return results, nil
}

// WatchHistory returns watch history from Tautulli (required for Plex history).
func (p *PlexServer) WatchHistory(limit int) ([]WatchEntry, error) {
	key := keys.Get("tautulli")
	if key == "" || !api.CheckReachable("tautulli") {
		return nil, fmt.Errorf("Tautulli is required for Plex watch history but is not available")
	}
	return tautulliHistory(key, limit)
}
