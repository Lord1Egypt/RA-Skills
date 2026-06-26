package arr

import (
	"encoding/json"
	"fmt"
	"time"

	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/config"
)

// Client provides typed access to *Arr service APIs.
type Client struct {
	api     *api.Client
	service string
	ver     string
}

// New creates a Client for the given *Arr service (radarr, sonarr, prowlarr, etc.).
func New(service string) *Client {
	return &Client{
		api:     api.NewClient(service),
		service: service,
		ver:     config.ServiceAPIVer(service),
	}
}

func (c *Client) endpoint(path string) string {
	return fmt.Sprintf("api/%s/%s", c.ver, path)
}

// Service returns the service name this client is bound to.
func (c *Client) Service() string {
	return c.service
}

// --- Radarr ---

// Movies fetches all movies from Radarr.
func (c *Client) Movies() ([]Movie, error) {
	var data []Movie
	err := c.api.GetJSON(c.endpoint("movie"), nil, &data)
	return data, err
}

// LookupMovie searches Radarr for movies matching the query.
func (c *Client) LookupMovie(query string) ([]map[string]interface{}, error) {
	var data []map[string]interface{}
	err := c.api.GetJSON(c.endpoint("movie/lookup"), map[string]string{"term": query}, &data)
	return data, err
}

// AddMovie adds a movie to Radarr.
func (c *Client) AddMovie(data map[string]interface{}) (map[string]interface{}, error) {
	body, err := c.api.Post(c.endpoint("movie"), data, nil)
	if err != nil {
		return nil, err
	}
	var result map[string]interface{}
	err = json.Unmarshal(body, &result)
	return result, err
}

// Releases fetches available releases for a movie.
func (c *Client) Releases(movieID int) ([]Release, error) {
	var data []Release
	params := map[string]string{"movieId": fmt.Sprintf("%d", movieID)}
	err := c.api.GetJSON(c.endpoint("release"), params, &data, 30*time.Second)
	return data, err
}

// --- Sonarr ---

// Series fetches all series from Sonarr.
func (c *Client) Series() ([]Series, error) {
	var data []Series
	err := c.api.GetJSON(c.endpoint("series"), nil, &data)
	return data, err
}

// LookupSeries searches Sonarr for series matching the query.
func (c *Client) LookupSeries(query string) ([]map[string]interface{}, error) {
	var data []map[string]interface{}
	err := c.api.GetJSON(c.endpoint("series/lookup"), map[string]string{"term": query}, &data)
	return data, err
}

// AddSeries adds a series to Sonarr.
func (c *Client) AddSeries(data map[string]interface{}) (map[string]interface{}, error) {
	body, err := c.api.Post(c.endpoint("series"), data, nil)
	if err != nil {
		return nil, err
	}
	var result map[string]interface{}
	err = json.Unmarshal(body, &result)
	return result, err
}

// WantedMissing fetches missing episodes from Sonarr.
func (c *Client) WantedMissing(pageSize int, extraParams map[string]string) (*WantedMissingPage, error) {
	params := map[string]string{"pageSize": fmt.Sprintf("%d", pageSize)}
	for k, v := range extraParams {
		params[k] = v
	}
	var data WantedMissingPage
	err := c.api.GetJSON(c.endpoint("wanted/missing"), params, &data)
	return &data, err
}

// --- Shared ---

// Queue fetches the import queue.
func (c *Client) Queue(pageSize int) (*QueuePage, error) {
	var data QueuePage
	params := map[string]string{"pageSize": fmt.Sprintf("%d", pageSize)}
	err := c.api.GetJSON(c.endpoint("queue"), params, &data)
	return &data, err
}

// Health fetches health warnings.
func (c *Client) Health() ([]HealthItem, error) {
	var data []HealthItem
	err := c.api.GetJSON(c.endpoint("health"), nil, &data)
	return data, err
}

// RootFolders fetches configured root folders.
func (c *Client) RootFolders() ([]RootFolder, error) {
	var data []RootFolder
	err := c.api.GetJSON(c.endpoint("rootfolder"), nil, &data)
	return data, err
}

// AddRootFolder creates a new root folder.
func (c *Client) AddRootFolder(path string) error {
	_, err := c.api.Post(c.endpoint("rootfolder"), map[string]string{"path": path}, nil)
	return err
}

// QualityProfiles fetches available quality profiles.
func (c *Client) QualityProfiles() ([]QualityProfile, error) {
	var data []QualityProfile
	err := c.api.GetJSON(c.endpoint("qualityprofile"), nil, &data)
	return data, err
}

// CustomFormats fetches all custom formats from a *Arr service.
func (c *Client) CustomFormats() ([]CustomFormat, error) {
	var data []CustomFormat
	err := c.api.GetJSON(c.endpoint("customformat"), nil, &data)
	return data, err
}

// Commands fetches active commands/tasks.
func (c *Client) Commands() ([]Command, error) {
	var data []Command
	err := c.api.GetJSON(c.endpoint("command"), nil, &data)
	return data, err
}

// GetJSON is a pass-through for arbitrary endpoints on this service.
func (c *Client) GetJSON(endpoint string, params map[string]string, target interface{}, timeout ...time.Duration) error {
	return c.api.GetJSON(endpoint, params, target, timeout...)
}

// Get is a pass-through for arbitrary GET endpoints on this service.
func (c *Client) Get(endpoint string, params map[string]string, timeout ...time.Duration) ([]byte, error) {
	return c.api.Get(endpoint, params, timeout...)
}

// Post is a pass-through for arbitrary POST endpoints on this service.
func (c *Client) Post(endpoint string, body interface{}, params map[string]string, timeout ...time.Duration) ([]byte, error) {
	return c.api.Post(endpoint, body, params, timeout...)
}

// Put is a pass-through for arbitrary PUT endpoints on this service.
func (c *Client) Put(endpoint string, body interface{}, params map[string]string, timeout ...time.Duration) ([]byte, error) {
	return c.api.Put(endpoint, body, params, timeout...)
}

// Delete is a pass-through for arbitrary DELETE endpoints on this service.
func (c *Client) Delete(endpoint string, params map[string]string, timeout ...time.Duration) ([]byte, error) {
	return c.api.Delete(endpoint, params, timeout...)
}

// --- Prowlarr ---

// Search performs a Prowlarr indexer search.
func (c *Client) Search(query string) ([]SearchResult, error) {
	var data []SearchResult
	params := map[string]string{"query": query, "type": "search"}
	err := c.api.GetJSON(c.endpoint("search"), params, &data, 30*time.Second)
	return data, err
}

// Indexers fetches all configured indexers from Prowlarr.
func (c *Client) Indexers() ([]Indexer, error) {
	var data []Indexer
	err := c.api.GetJSON(c.endpoint("indexer"), nil, &data)
	return data, err
}

// IndexerStatuses fetches indexer status info from Prowlarr.
func (c *Client) IndexerStatuses() ([]IndexerStatus, error) {
	var data []IndexerStatus
	err := c.api.GetJSON(c.endpoint("indexerstatus"), nil, &data)
	return data, err
}

// AddIndexer adds an indexer to Prowlarr.
func (c *Client) AddIndexer(data map[string]interface{}) (Indexer, error) {
	body, err := c.api.Post(c.endpoint("indexer"), data, nil)
	if err != nil {
		return Indexer{}, err
	}
	var result Indexer
	err = json.Unmarshal(body, &result)
	return result, err
}

// UpdateIndexer updates an existing indexer.
func (c *Client) UpdateIndexer(id int, data interface{}) error {
	_, err := c.api.Put(c.endpoint(fmt.Sprintf("indexer/%d", id)), data, nil)
	return err
}

// DeleteIndexer deletes an indexer by ID.
func (c *Client) DeleteIndexer(id int) error {
	_, err := c.api.Delete(c.endpoint(fmt.Sprintf("indexer/%d", id)), nil)
	return err
}

// TestAllIndexers tests all Prowlarr indexers.
func (c *Client) TestAllIndexers() ([]IndexerTestResult, error) {
	body, err := c.api.Post(c.endpoint("indexer/testall"), nil, nil, 120*time.Second)
	if err != nil {
		return nil, err
	}
	var data []IndexerTestResult
	err = json.Unmarshal(body, &data)
	return data, err
}

// IndexerProxies fetches indexer proxy configurations.
func (c *Client) IndexerProxies() ([]struct{ Tags []int `json:"tags"` }, error) {
	var data []struct {
		Tags []int `json:"tags"`
	}
	err := c.api.GetJSON(c.endpoint("indexerProxy"), nil, &data)
	return data, err
}

// Applications fetches Prowlarr application sync targets.
func (c *Client) Applications() ([]struct {
	ID             int    `json:"id"`
	Name           string `json:"name"`
	Implementation string `json:"implementation"`
	SyncLevel      string `json:"syncLevel"`
}, error) {
	var data []struct {
		ID             int    `json:"id"`
		Name           string `json:"name"`
		Implementation string `json:"implementation"`
		SyncLevel      string `json:"syncLevel"`
	}
	err := c.api.GetJSON(c.endpoint("applications"), nil, &data)
	return data, err
}

// --- Download Clients ---

// DownloadClients fetches all download clients.
func (c *Client) DownloadClients() ([]DownloadClient, error) {
	var data []DownloadClient
	err := c.api.GetJSON(c.endpoint("downloadclient"), nil, &data)
	return data, err
}

// DownloadClientSchemas fetches available download client schemas.
func (c *Client) DownloadClientSchemas() ([]DownloadClient, error) {
	var data []DownloadClient
	err := c.api.GetJSON(c.endpoint("downloadclient/schema"), nil, &data)
	return data, err
}

// CreateDownloadClient creates a new download client.
func (c *Client) CreateDownloadClient(dc *DownloadClient) error {
	_, err := c.api.Post(c.endpoint("downloadclient"), dc, nil)
	return err
}

// UpdateDownloadClient updates an existing download client.
func (c *Client) UpdateDownloadClient(dc *DownloadClient) error {
	_, err := c.api.Put(c.endpoint(fmt.Sprintf("downloadclient/%d", dc.ID)), dc, nil)
	return err
}

// GetMovieByID fetches a single movie by ID (for full payload before PUT).
func (c *Client) GetMovieByID(id int) (map[string]interface{}, error) {
	var data map[string]interface{}
	err := c.api.GetJSON(c.endpoint(fmt.Sprintf("movie/%d", id)), nil, &data)
	return data, err
}

// UpdateMovie updates a movie via PUT.
func (c *Client) UpdateMovie(id int, data map[string]interface{}) error {
	_, err := c.api.Put(c.endpoint(fmt.Sprintf("movie/%d", id)), data, nil)
	return err
}

// GetSeriesByID fetches a single series by ID.
func (c *Client) GetSeriesByID(id int) (map[string]interface{}, error) {
	var data map[string]interface{}
	err := c.api.GetJSON(c.endpoint(fmt.Sprintf("series/%d", id)), nil, &data)
	return data, err
}

// UpdateSeries updates a series via PUT.
func (c *Client) UpdateSeries(id int, data map[string]interface{}) error {
	_, err := c.api.Put(c.endpoint(fmt.Sprintf("series/%d", id)), data, nil)
	return err
}

// GetIndexerByID fetches a single indexer by ID.
func (c *Client) GetIndexerByID(id int) (map[string]interface{}, error) {
	var data map[string]interface{}
	err := c.api.GetJSON(c.endpoint(fmt.Sprintf("indexer/%d", id)), nil, &data)
	return data, err
}
