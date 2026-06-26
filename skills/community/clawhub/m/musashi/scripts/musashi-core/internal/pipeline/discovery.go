package pipeline

import (
	"encoding/json"
	"fmt"

	"github.com/yeheskieltame/musashi/scripts/musashi-core/internal/data"
)

// DiscoveryResult holds discovered tokens.
type DiscoveryResult struct {
	Chain  int64           `json:"chain_id"`
	Tokens []DiscoveredToken `json:"tokens"`
}

type DiscoveredToken struct {
	Address   string  `json:"address"`
	Name      string  `json:"name"`
	Symbol    string  `json:"symbol"`
	PriceUsd  string  `json:"price_usd"`
	Volume24h float64 `json:"volume_24h"`
	Liquidity float64 `json:"liquidity_usd"`
	Source    string  `json:"source"`
}

// DiscoverTokens scans for new tokens using GeckoTerminal and DexScreener.
func DiscoverTokens(chainID int64, limit int) (string, error) {
	result := &DiscoveryResult{
		Chain:  chainID,
		Tokens: make([]DiscoveredToken, 0),
	}

	network := data.ChainIDToNetwork(chainID)
	gecko := data.NewGeckoTerminalClient()

	// Source 1: New pools on the chain
	newPools, err := gecko.GetNewPools(network)
	if err == nil {
		for _, pool := range newPools {
			if len(result.Tokens) >= limit {
				break
			}
			result.Tokens = append(result.Tokens, DiscoveredToken{
				Address:   pool.Attributes.Address,
				Name:      pool.Attributes.Name,
				PriceUsd:  pool.Attributes.BaseTokenPrice,
				Liquidity: parseFloat(pool.Attributes.ReserveUsd),
				Source:    "geckoterminal_new_pools",
			})
		}
	}

	// Source 2: Trending pools
	if len(result.Tokens) < limit {
		trending, err := gecko.GetTrendingPools()
		if err == nil {
			for _, pool := range trending {
				if len(result.Tokens) >= limit {
					break
				}
				result.Tokens = append(result.Tokens, DiscoveredToken{
					Address:   pool.Attributes.Address,
					Name:      pool.Attributes.Name,
					PriceUsd:  pool.Attributes.BaseTokenPrice,
					Liquidity: parseFloat(pool.Attributes.ReserveUsd),
					Source:    "geckoterminal_trending",
				})
			}
		}
	}

	b, _ := json.MarshalIndent(result, "", "  ")
	return string(b), nil
}

func parseFloat(s string) float64 {
	var f float64
	fmt.Sscanf(s, "%f", &f)
	return f
}
