package data

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

const coinGeckoBaseURL = "https://api.coingecko.com/api/v3"

type CoinGeckoClient struct {
	client *http.Client
}

func NewCoinGeckoClient() *CoinGeckoClient {
	return &CoinGeckoClient{
		client: &http.Client{Timeout: 15 * time.Second},
	}
}

type GlobalData struct {
	Data struct {
		TotalMarketCap          map[string]float64 `json:"total_market_cap"`
		TotalVolume             map[string]float64 `json:"total_volume"`
		MarketCapPercentage     map[string]float64 `json:"market_cap_percentage"`
		MarketCapChangePerc24h  float64            `json:"market_cap_change_percentage_24h_usd"`
	} `json:"data"`
}

type TrendingResponse struct {
	Coins []struct {
		Item struct {
			ID            string  `json:"id"`
			CoinID        int     `json:"coin_id"`
			Name          string  `json:"name"`
			Symbol        string  `json:"symbol"`
			MarketCapRank int     `json:"market_cap_rank"`
			Score         int     `json:"score"`
			PriceBTC      float64 `json:"price_btc"`
		} `json:"item"`
	} `json:"coins"`
}

type CoinCategory struct {
	ID                string  `json:"id"`
	Name              string  `json:"name"`
	MarketCap         float64 `json:"market_cap"`
	MarketCapChange24h float64 `json:"market_cap_change_24h"`
	Volume24h         float64 `json:"volume_24h"`
	Top3Coins         []string `json:"top_3_coins"`
}

// GetGlobal fetches global market data (total market cap, BTC dominance).
func (c *CoinGeckoClient) GetGlobal() (*GlobalData, error) {
	url := fmt.Sprintf("%s/global", coinGeckoBaseURL)

	resp, err := c.client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("coingecko request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("coingecko error: status %d: %s", resp.StatusCode, body)
	}

	var result GlobalData
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("coingecko decode failed: %w", err)
	}

	return &result, nil
}

// GetTrending fetches trending coins.
func (c *CoinGeckoClient) GetTrending() (*TrendingResponse, error) {
	url := fmt.Sprintf("%s/search/trending", coinGeckoBaseURL)

	resp, err := c.client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("coingecko request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("coingecko error: status %d: %s", resp.StatusCode, body)
	}

	var result TrendingResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("coingecko decode failed: %w", err)
	}

	return &result, nil
}

// GetCategories fetches coin categories with market data.
func (c *CoinGeckoClient) GetCategories() ([]CoinCategory, error) {
	url := fmt.Sprintf("%s/coins/categories", coinGeckoBaseURL)

	resp, err := c.client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("coingecko request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("coingecko error: status %d: %s", resp.StatusCode, body)
	}

	var result []CoinCategory
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("coingecko decode failed: %w", err)
	}

	return result, nil
}
