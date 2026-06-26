package qbit

import (
	"fmt"
	"net/http"
	"net/url"
	"strings"
	"time"

	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/config"
)

// Client provides typed access to the qBittorrent API.
type Client struct {
	api *api.Client
}

// New creates a qBittorrent client.
func New() *Client {
	return &Client{api: api.NewClient("qbittorrent")}
}

// Torrents fetches all torrents from qBittorrent.
func (c *Client) Torrents() ([]Torrent, error) {
	var data []Torrent
	err := c.api.GetJSON("api/v2/torrents/info", nil, &data)
	return data, err
}

// Preferences fetches qBittorrent application preferences.
func (c *Client) Preferences() (*Preferences, error) {
	var prefs Preferences
	err := c.api.GetJSON("api/v2/app/preferences", nil, &prefs)
	return &prefs, err
}

// SetPreferences updates qBittorrent preferences.
// Accepts a JSON-encodable map of preference keys to set.
func (c *Client) SetPreferences(prefs map[string]interface{}) error {
	_, err := c.api.Post("api/v2/app/setPreferences", prefs, nil)
	return err
}

// Version returns the qBittorrent application version string.
func (c *Client) Version() (string, error) {
	data, err := c.api.Get("api/v2/app/version", nil)
	if err != nil {
		return "", err
	}
	return strings.TrimSpace(string(data)), nil
}

// Pause pauses torrents by hash. Use "all" to pause all.
func (c *Client) Pause(hashes ...string) error {
	return c.postHashes("api/v2/torrents/pause", hashes)
}

// Resume resumes torrents by hash. Use "all" to resume all.
func (c *Client) Resume(hashes ...string) error {
	return c.postHashes("api/v2/torrents/resume", hashes)
}

// Delete removes torrents by hash. If deleteFiles is true, also deletes data.
func (c *Client) Delete(deleteFiles bool, hashes ...string) error {
	h := strings.Join(hashes, "|")
	del := "false"
	if deleteFiles {
		del = "true"
	}

	qbitURL := config.ServiceURL("qbittorrent")
	params := url.Values{}
	params.Set("hashes", h)
	params.Set("deleteFiles", del)

	req, err := http.NewRequest("POST", qbitURL+"/api/v2/torrents/delete", strings.NewReader(params.Encode()))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	resp, err := (&http.Client{Timeout: 5 * time.Second}).Do(req)
	if err != nil {
		return err
	}
	resp.Body.Close()
	return nil
}

// Categories fetches all torrent categories.
func (c *Client) Categories() (map[string]Category, error) {
	var cats map[string]Category
	err := c.api.GetJSON("api/v2/torrents/categories", nil, &cats)
	return cats, err
}

// postHashes posts a hash-based action (pause, resume, recheck, etc.)
func (c *Client) postHashes(endpoint string, hashes []string) error {
	h := strings.Join(hashes, "|")
	qbitURL := config.ServiceURL("qbittorrent")

	params := url.Values{}
	params.Set("hashes", h)

	req, err := http.NewRequest("POST", qbitURL+"/"+endpoint, strings.NewReader(params.Encode()))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	resp, err := (&http.Client{Timeout: 5 * time.Second}).Do(req)
	if err != nil {
		return err
	}
	resp.Body.Close()

	if resp.StatusCode >= 400 {
		return fmt.Errorf("qBittorrent returned %d", resp.StatusCode)
	}
	return nil
}
