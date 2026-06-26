package data

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"time"
)

const neynarBaseURL = "https://api.neynar.com/v2/farcaster"

type FarcasterClient struct {
	client *http.Client
	apiKey string
}

func NewFarcasterClient(apiKey string) *FarcasterClient {
	if apiKey == "" {
		apiKey = "NEYNAR_API_DOCS" // public demo key
	}
	return &FarcasterClient{
		client: &http.Client{Timeout: 15 * time.Second},
		apiKey: apiKey,
	}
}

type FarcasterCast struct {
	Hash      string `json:"hash"`
	Text      string `json:"text"`
	Timestamp string `json:"timestamp"`
	Author    struct {
		FID         int    `json:"fid"`
		Username    string `json:"username"`
		DisplayName string `json:"display_name"`
		Followers   int    `json:"follower_count"`
	} `json:"author"`
	Reactions struct {
		Likes   int `json:"likes_count"`
		Recasts int `json:"recasts_count"`
	} `json:"reactions"`
	Replies struct {
		Count int `json:"count"`
	} `json:"replies"`
}

type FarcasterSearchResponse struct {
	Result struct {
		Casts []FarcasterCast `json:"casts"`
	} `json:"result"`
}

// SearchCasts searches Farcaster for casts mentioning a query.
func (c *FarcasterClient) SearchCasts(query string) ([]FarcasterCast, error) {
	u := fmt.Sprintf("%s/cast/search?q=%s&limit=25", neynarBaseURL, url.QueryEscape(query))

	req, err := http.NewRequest("GET", u, nil)
	if err != nil {
		return nil, fmt.Errorf("farcaster request build failed: %w", err)
	}
	req.Header.Set("accept", "application/json")
	req.Header.Set("api_key", c.apiKey)

	resp, err := c.client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("farcaster request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("farcaster error: status %d: %s", resp.StatusCode, body)
	}

	var result FarcasterSearchResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("farcaster decode failed: %w", err)
	}

	return result.Result.Casts, nil
}
