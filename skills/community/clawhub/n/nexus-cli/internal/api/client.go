package api

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"
	"time"

	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/keys"
)

var client = &http.Client{Timeout: 5 * time.Second}

// Client is a service-bound API client that avoids repeating the service name.
type Client struct {
	Service string
}

// NewClient creates a Client bound to the given service name.
func NewClient(service string) *Client {
	return &Client{Service: service}
}

func (c *Client) Get(endpoint string, params map[string]string, timeout ...time.Duration) ([]byte, error) {
	return Get(c.Service, endpoint, params, timeout...)
}

func (c *Client) GetJSON(endpoint string, params map[string]string, target interface{}, timeout ...time.Duration) error {
	return GetJSON(c.Service, endpoint, params, target, timeout...)
}

func (c *Client) Post(endpoint string, body interface{}, params map[string]string, timeout ...time.Duration) ([]byte, error) {
	return Post(c.Service, endpoint, body, params, timeout...)
}

func (c *Client) PostJSON(endpoint string, body interface{}, params map[string]string, target interface{}, timeout ...time.Duration) error {
	return PostJSON(c.Service, endpoint, body, params, target, timeout...)
}

func (c *Client) Put(endpoint string, body interface{}, params map[string]string, timeout ...time.Duration) ([]byte, error) {
	return Put(c.Service, endpoint, body, params, timeout...)
}

func (c *Client) PutJSON(endpoint string, body interface{}, params map[string]string, target interface{}, timeout ...time.Duration) error {
	return PutJSON(c.Service, endpoint, body, params, target, timeout...)
}

func (c *Client) Delete(endpoint string, params map[string]string, timeout ...time.Duration) ([]byte, error) {
	return Delete(c.Service, endpoint, params, timeout...)
}

// Get performs an authenticated GET request to a service endpoint.
// Returns the raw body bytes and any error.
func Get(service, endpoint string, params map[string]string, timeout ...time.Duration) ([]byte, error) {
	t := 5 * time.Second
	if len(timeout) > 0 {
		t = timeout[0]
	}

	c := &http.Client{Timeout: t}
	u := buildURL(service, endpoint, params)

	req, err := http.NewRequest("GET", u, nil)
	if err != nil {
		return nil, err
	}
	addAuth(req, service)

	resp, err := c.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	return io.ReadAll(resp.Body)
}

// GetJSON performs an authenticated GET and unmarshals the JSON response.
func GetJSON(service, endpoint string, params map[string]string, target interface{}, timeout ...time.Duration) error {
	data, err := Get(service, endpoint, params, timeout...)
	if err != nil {
		return err
	}
	return json.Unmarshal(data, target)
}

// Post performs an authenticated POST request with a JSON body.
func Post(service, endpoint string, body interface{}, params map[string]string, timeout ...time.Duration) ([]byte, error) {
	t := 10 * time.Second
	if len(timeout) > 0 {
		t = timeout[0]
	}

	c := &http.Client{Timeout: t}
	u := buildURL(service, endpoint, params)

	var bodyReader io.Reader
	if body != nil {
		data, err := json.Marshal(body)
		if err != nil {
			return nil, err
		}
		bodyReader = strings.NewReader(string(data))
	}

	req, err := http.NewRequest("POST", u, bodyReader)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", "application/json")
	addAuth(req, service)

	resp, err := c.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	return io.ReadAll(resp.Body)
}

// PostJSON performs an authenticated POST and unmarshals the JSON response.
func PostJSON(service, endpoint string, body interface{}, params map[string]string, target interface{}, timeout ...time.Duration) error {
	data, err := Post(service, endpoint, body, params, timeout...)
	if err != nil {
		return err
	}
	return json.Unmarshal(data, target)
}

// Put performs an authenticated PUT request with a JSON body.
func Put(service, endpoint string, body interface{}, params map[string]string, timeout ...time.Duration) ([]byte, error) {
	t := 10 * time.Second
	if len(timeout) > 0 {
		t = timeout[0]
	}

	c := &http.Client{Timeout: t}
	u := buildURL(service, endpoint, params)

	var bodyReader io.Reader
	if body != nil {
		data, err := json.Marshal(body)
		if err != nil {
			return nil, err
		}
		bodyReader = strings.NewReader(string(data))
	}

	req, err := http.NewRequest("PUT", u, bodyReader)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", "application/json")
	addAuth(req, service)

	resp, err := c.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	return io.ReadAll(resp.Body)
}

// PutJSON performs an authenticated PUT and unmarshals the JSON response.
func PutJSON(service, endpoint string, body interface{}, params map[string]string, target interface{}, timeout ...time.Duration) error {
	data, err := Put(service, endpoint, body, params, timeout...)
	if err != nil {
		return err
	}
	return json.Unmarshal(data, target)
}

// Delete performs an authenticated DELETE request.
func Delete(service, endpoint string, params map[string]string, timeout ...time.Duration) ([]byte, error) {
	t := 5 * time.Second
	if len(timeout) > 0 {
		t = timeout[0]
	}

	c := &http.Client{Timeout: t}
	u := buildURL(service, endpoint, params)

	req, err := http.NewRequest("DELETE", u, nil)
	if err != nil {
		return nil, err
	}
	addAuth(req, service)

	resp, err := c.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	return io.ReadAll(resp.Body)
}

// CheckReachable checks if a service is reachable.
func CheckReachable(service string) bool {
	def, hasDef := config.GetServiceDef(service)

	// Skip services without an API or without a port
	if hasDef && (!def.HasAPI || def.Port == 0) {
		return false
	}

	ep := healthEndpoint(service, def, hasDef)

	u := fmt.Sprintf("%s/%s", config.ServiceURL(service), ep)
	c := &http.Client{Timeout: 3 * time.Second}
	resp, err := c.Get(u)
	if err != nil {
		return false
	}
	resp.Body.Close()
	return resp.StatusCode >= 200 && resp.StatusCode < 500
}

// healthEndpoint derives a health-check path from the service registry.
func healthEndpoint(service string, def config.ServiceDef, hasDef bool) string {
	// Service-specific overrides that can't be derived from registry fields
	switch service {
	case "jellyfin":
		return "System/Info/Public"
	case "plex":
		return "identity"
	case "qbittorrent":
		return "api/v2/app/version"
	case "sabnzbd":
		return fmt.Sprintf("api?mode=version&apikey=%s&output=json", keys.Get(service))
	case "tautulli":
		return fmt.Sprintf("api/v2?apikey=%s&cmd=status", keys.Get(service))
	case "seerr":
		return "api/v1/status"
	case "gluetun":
		return "v1/publicip/ip"
	case "tdarr":
		return "api/v2/status"
	case "jellystat":
		return "api/status"
	case "notifiarr":
		return "api/version"
	case "autobrr":
		return "api/healthz"
	}

	// *Arr services (management + indexer categories with APIVer) use api/{ver}/health
	if hasDef && def.APIVer != "" {
		return fmt.Sprintf("api/%s/health?apikey=%s", def.APIVer, keys.Get(service))
	}

	// Default: try root
	return ""
}

func buildURL(service, endpoint string, params map[string]string) string {
	key := keys.Get(service)
	p := make(url.Values)

	// Add API key as query param for *Arr services (services with an APIVer)
	if key != "" {
		if def, ok := config.GetServiceDef(service); ok && def.APIVer != "" {
			p.Set("apikey", key)
		}
	}

	for k, v := range params {
		p.Set(k, v)
	}

	u := fmt.Sprintf("%s/%s", config.ServiceURL(service), endpoint)
	if encoded := p.Encode(); encoded != "" {
		u += "?" + encoded
	}
	return u
}

func addAuth(req *http.Request, service string) {
	key := keys.Get(service)
	if key == "" {
		return
	}
	// Auth style varies per service; the registry doesn't encode header format,
	// so we keep explicit cases for services with non-standard auth headers.
	switch service {
	case "jellyfin":
		req.Header.Set("X-Emby-Token", key)
	case "plex":
		req.Header.Set("X-Plex-Token", key)
		req.Header.Set("Accept", "application/json")
	case "bazarr":
		req.Header.Set("X-API-KEY", key)
	case "tautulli":
		// Tautulli uses apikey as a query param; no header needed.
	case "sabnzbd":
		// SABnzbd uses apikey as a query param; no header needed.
	case "notifiarr":
		req.Header.Set("x-api-key", key)
	default:
		// *Arr services (with APIVer) use query-param auth via buildURL.
		// Other API services with a key (seerr, autobrr, etc.) use X-Api-Key header.
		if def, ok := config.GetServiceDef(service); ok {
			if def.APIVer != "" {
				return // already handled by buildURL
			}
			if def.HasAPI && def.KeySource != "none" {
				req.Header.Set("X-Api-Key", key)
			}
		}
	}
}
