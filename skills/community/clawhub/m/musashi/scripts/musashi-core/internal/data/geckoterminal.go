package data

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

const geckoTerminalBaseURL = "https://api.geckoterminal.com/api/v2"

type GeckoTerminalClient struct {
	client *http.Client
}

func NewGeckoTerminalClient() *GeckoTerminalClient {
	return &GeckoTerminalClient{
		client: &http.Client{Timeout: 15 * time.Second},
	}
}

// GeckoResponse wraps the standard JSON:API response.
type GeckoResponse struct {
	Data json.RawMessage `json:"data"`
}

type GeckoTokenAttributes struct {
	Name         string  `json:"name"`
	Symbol       string  `json:"symbol"`
	Address      string  `json:"address"`
	PriceUsd     string  `json:"price_usd"`
	Volume24h    string  `json:"volume_usd_h24"`
	MarketCapUsd string  `json:"market_cap_usd"`
	FDVUsd       string  `json:"fdv_usd"`
}

type GeckoTokenData struct {
	ID         string               `json:"id"`
	Type       string               `json:"type"`
	Attributes GeckoTokenAttributes `json:"attributes"`
}

type GeckoPoolAttributes struct {
	Name            string `json:"name"`
	Address         string `json:"address"`
	BaseTokenPrice  string `json:"base_token_price_usd"`
	QuoteTokenPrice string `json:"quote_token_price_usd"`
	VolumeH24       string `json:"volume_usd_h24"`
	ReserveUsd      string `json:"reserve_in_usd"`
	PoolCreatedAt   string `json:"pool_created_at"`
}

type GeckoPoolData struct {
	ID         string              `json:"id"`
	Type       string              `json:"type"`
	Attributes GeckoPoolAttributes `json:"attributes"`
}

// ChainIDToNetwork maps EVM chain IDs to GeckoTerminal network slugs.
func ChainIDToNetwork(chainID int64) string {
	switch chainID {
	case 1:
		return "eth"
	case 56:
		return "bsc"
	case 137:
		return "polygon_pos"
	case 42161:
		return "arbitrum"
	case 8453:
		return "base"
	default:
		return "eth"
	}
}

// GetToken fetches token data.
func (c *GeckoTerminalClient) GetToken(network, address string) (*GeckoTokenData, error) {
	url := fmt.Sprintf("%s/networks/%s/tokens/%s", geckoTerminalBaseURL, network, address)

	resp, err := c.client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("geckoterminal request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("geckoterminal error: status %d: %s", resp.StatusCode, body)
	}

	var raw struct {
		Data GeckoTokenData `json:"data"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&raw); err != nil {
		return nil, fmt.Errorf("geckoterminal decode failed: %w", err)
	}

	return &raw.Data, nil
}

// GetTokenPools fetches all pools for a token.
func (c *GeckoTerminalClient) GetTokenPools(network, address string) ([]GeckoPoolData, error) {
	url := fmt.Sprintf("%s/networks/%s/tokens/%s/pools", geckoTerminalBaseURL, network, address)

	resp, err := c.client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("geckoterminal request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("geckoterminal error: status %d: %s", resp.StatusCode, body)
	}

	var raw struct {
		Data []GeckoPoolData `json:"data"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&raw); err != nil {
		return nil, fmt.Errorf("geckoterminal decode failed: %w", err)
	}

	return raw.Data, nil
}

// GetNewPools fetches newly created pools on a network.
func (c *GeckoTerminalClient) GetNewPools(network string) ([]GeckoPoolData, error) {
	url := fmt.Sprintf("%s/networks/%s/new_pools", geckoTerminalBaseURL, network)

	resp, err := c.client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("geckoterminal request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("geckoterminal error: status %d: %s", resp.StatusCode, body)
	}

	var raw struct {
		Data []GeckoPoolData `json:"data"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&raw); err != nil {
		return nil, fmt.Errorf("geckoterminal decode failed: %w", err)
	}

	return raw.Data, nil
}

// GetTrendingPools fetches trending pools across all networks.
func (c *GeckoTerminalClient) GetTrendingPools() ([]GeckoPoolData, error) {
	url := fmt.Sprintf("%s/networks/trending_pools", geckoTerminalBaseURL)

	resp, err := c.client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("geckoterminal request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("geckoterminal error: status %d: %s", resp.StatusCode, body)
	}

	var raw struct {
		Data []GeckoPoolData `json:"data"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&raw); err != nil {
		return nil, fmt.Errorf("geckoterminal decode failed: %w", err)
	}

	return raw.Data, nil
}
