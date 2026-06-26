package data

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

const defiLlamaBaseURL = "https://api.llama.fi"

type DefiLlamaClient struct {
	client *http.Client
}

func NewDefiLlamaClient() *DefiLlamaClient {
	return &DefiLlamaClient{
		client: &http.Client{Timeout: 15 * time.Second},
	}
}

type ChainTVL struct {
	Name  string  `json:"name"`
	TVL   float64 `json:"tvl"`
	Gecko string  `json:"gecko_id"`
}

type HistoricalTVL struct {
	Date float64 `json:"date"`
	TVL  float64 `json:"tvl"`
}

type Stablecoin struct {
	ID        string `json:"id"`
	Name      string `json:"name"`
	Symbol    string `json:"symbol"`
	PegType   string `json:"pegType"`
	CirculatingPrevDay json.RawMessage `json:"circulatingPrevDay"`
	Circulating        json.RawMessage `json:"circulating"`
}

type StablecoinChainData struct {
	Gecko      string             `json:"gecko_id"`
	TotalCirc  map[string]float64 `json:"totalCirculatingUSD"`
}

// GetChains fetches all chains with current TVL.
func (c *DefiLlamaClient) GetChains() ([]ChainTVL, error) {
	url := fmt.Sprintf("%s/v2/chains", defiLlamaBaseURL)

	resp, err := c.client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("defillama request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("defillama error: status %d: %s", resp.StatusCode, body)
	}

	var chains []ChainTVL
	if err := json.NewDecoder(resp.Body).Decode(&chains); err != nil {
		return nil, fmt.Errorf("defillama decode failed: %w", err)
	}

	return chains, nil
}

// GetHistoricalChainTVL fetches historical TVL for a chain.
func (c *DefiLlamaClient) GetHistoricalChainTVL(chain string) ([]HistoricalTVL, error) {
	url := fmt.Sprintf("%s/v2/historicalChainTvl/%s", defiLlamaBaseURL, chain)

	resp, err := c.client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("defillama request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("defillama error: status %d: %s", resp.StatusCode, body)
	}

	var history []HistoricalTVL
	if err := json.NewDecoder(resp.Body).Decode(&history); err != nil {
		return nil, fmt.Errorf("defillama decode failed: %w", err)
	}

	return history, nil
}

// GetStablecoins fetches all stablecoins with circulating data.
func (c *DefiLlamaClient) GetStablecoins() ([]Stablecoin, error) {
	url := fmt.Sprintf("%s/stablecoins", defiLlamaBaseURL)

	resp, err := c.client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("defillama request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("defillama error: status %d: %s", resp.StatusCode, body)
	}

	var raw struct {
		PeggedAssets []Stablecoin `json:"peggedAssets"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&raw); err != nil {
		return nil, fmt.Errorf("defillama decode failed: %w", err)
	}

	return raw.PeggedAssets, nil
}

// GetStablecoinChains fetches stablecoin distribution per chain.
func (c *DefiLlamaClient) GetStablecoinChains() ([]json.RawMessage, error) {
	url := fmt.Sprintf("%s/stablecoins/chains", defiLlamaBaseURL)

	resp, err := c.client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("defillama request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("defillama error: status %d: %s", resp.StatusCode, body)
	}

	var result []json.RawMessage
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("defillama decode failed: %w", err)
	}

	return result, nil
}

// ChainIDToDefiLlamaName maps chain IDs to DefiLlama chain names.
func ChainIDToDefiLlamaName(chainID int64) string {
	switch chainID {
	case 1:
		return "Ethereum"
	case 56:
		return "BSC"
	case 137:
		return "Polygon"
	case 42161:
		return "Arbitrum"
	case 8453:
		return "Base"
	default:
		return "Ethereum"
	}
}
