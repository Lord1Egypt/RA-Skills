package seerr

import (
	"fmt"

	"github.com/maxtechera/admirarr/internal/api"
)

// Client provides typed access to the Seerr API.
type Client struct {
	api *api.Client
}

// New creates a Seerr client.
func New() *Client {
	return &Client{api: api.NewClient("seerr")}
}

// Requests fetches media requests from Seerr.
func (c *Client) Requests(take int) (*RequestPage, error) {
	var data RequestPage
	params := map[string]string{"take": fmt.Sprintf("%d", take), "sort": "added"}
	err := c.api.GetJSON("api/v1/request", params, &data)
	return &data, err
}

// ResolveTitle fetches title and year for a media item from Seerr.
func (c *Client) ResolveTitle(mediaType string, tmdbID int) (title, year string) {
	endpoint := fmt.Sprintf("api/v1/%s/%d", mediaType, tmdbID)
	var info map[string]interface{}
	if err := c.api.GetJSON(endpoint, nil, &info); err != nil {
		return fmt.Sprintf("TMDB:%d", tmdbID), "?"
	}

	title = "?"
	if t, ok := info["title"].(string); ok && t != "" {
		title = t
	} else if t, ok := info["name"].(string); ok && t != "" {
		title = t
	}

	year = "?"
	if d, ok := info["releaseDate"].(string); ok && len(d) >= 4 {
		year = d[:4]
	} else if d, ok := info["firstAirDate"].(string); ok && len(d) >= 4 {
		year = d[:4]
	}

	return title, year
}
