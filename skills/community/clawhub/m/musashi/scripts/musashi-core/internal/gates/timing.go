package gates

import (
	"fmt"
	"github.com/yeheskieltame/musashi/scripts/musashi-core/internal/data"
)

// TimingGate implements Gate 6: Market Timing.
// Uses DefiLlama (chain TVL, stablecoin flows) + CoinGecko (global market data).
type TimingGate struct {
	defillama *data.DefiLlamaClient
	coingecko *data.CoinGeckoClient
}

func NewTimingGate() *TimingGate {
	return &TimingGate{
		defillama: data.NewDefiLlamaClient(),
		coingecko: data.NewCoinGeckoClient(),
	}
}

func (g *TimingGate) Name() string { return "Market Timing" }
func (g *TimingGate) Number() int  { return 6 }

func (g *TimingGate) Evaluate(token string, chainID int64) (*Result, error) {
	result := NewResult(g.Name(), g.Number())

	// Check 1: Global market health (BTC dominance + market cap change)
	global, err := g.coingecko.GetGlobal()
	if err != nil {
		result.AddEvidence("coingecko", "error", err.Error())
		// Don't fail — macro data is supplementary
	} else {
		btcDom := global.Data.MarketCapPercentage["btc"]
		mcapChange := global.Data.MarketCapChangePerc24h
		totalMcap := global.Data.TotalMarketCap["usd"]

		result.AddEvidence("coingecko", "btc_dominance", fmt.Sprintf("%.2f%%", btcDom))
		result.AddEvidence("coingecko", "market_cap_change_24h", fmt.Sprintf("%.2f%%", mcapChange))
		result.AddEvidence("coingecko", "total_market_cap_usd", fmt.Sprintf("%.0f", totalMcap))

		// Severe market downturn
		if mcapChange < -8.0 {
			return result.Fail(fmt.Sprintf("Market in freefall: %.1f%% 24h drop", mcapChange)), nil
		}

		// Very high BTC dominance = altcoin unfriendly
		if btcDom > 65.0 {
			result.AddEvidence("analysis", "btc_dominance_warning", "high — capital concentrated in BTC, altcoin rotation unlikely")
		}
	}

	// Check 2: Chain ecosystem health (TVL trend)
	chainName := data.ChainIDToDefiLlamaName(chainID)
	history, err := g.defillama.GetHistoricalChainTVL(chainName)
	if err != nil {
		result.AddEvidence("defillama", "tvl_error", err.Error())
	} else if len(history) >= 7 {
		// Compare last 7 days TVL trend
		recent := history[len(history)-1].TVL
		weekAgo := history[len(history)-7].TVL

		result.AddEvidence("defillama", "chain", chainName)
		result.AddEvidence("defillama", "current_tvl", fmt.Sprintf("%.0f", recent))
		result.AddEvidence("defillama", "7d_ago_tvl", fmt.Sprintf("%.0f", weekAgo))

		if weekAgo > 0 {
			tvlChange := (recent - weekAgo) / weekAgo * 100
			result.AddEvidence("defillama", "tvl_change_7d", fmt.Sprintf("%.2f%%", tvlChange))

			if tvlChange < -15.0 {
				return result.Fail(fmt.Sprintf("%s TVL declining sharply: %.1f%% in 7 days", chainName, tvlChange)), nil
			}
		}

		// Check for sustained decline (30 days if available)
		if len(history) >= 30 {
			monthAgo := history[len(history)-30].TVL
			if monthAgo > 0 {
				monthChange := (recent - monthAgo) / monthAgo * 100
				result.AddEvidence("defillama", "tvl_change_30d", fmt.Sprintf("%.2f%%", monthChange))

				if monthChange < -30.0 {
					return result.Fail(fmt.Sprintf("%s ecosystem in sustained decline: %.1f%% TVL loss in 30 days", chainName, monthChange)), nil
				}
			}
		}
	}

	// Check 3: Stablecoin flows (macro inflow/outflow signal)
	stablecoins, err := g.defillama.GetStablecoins()
	if err != nil {
		result.AddEvidence("defillama", "stablecoin_error", err.Error())
	} else {
		// Sum top stablecoin market caps for macro signal
		topStables := 0
		for _, s := range stablecoins {
			if topStables >= 5 {
				break
			}
			result.AddEvidence("defillama", fmt.Sprintf("stablecoin_%s", s.Symbol), s.Name)
			topStables++
		}
		result.AddEvidence("defillama", "stablecoin_count", fmt.Sprintf("%d", len(stablecoins)))
	}

	// Determine overall timing assessment
	warningCount := 0
	for _, e := range result.Evidence {
		if e.Key == "btc_dominance_warning" {
			warningCount++
		}
		if e.Key == "tvl_change_7d" {
			// Parse back
			var val float64
			fmt.Sscanf(e.Value, "%f%%", &val)
			if val < -5.0 {
				warningCount++
			}
		}
	}

	if warningCount >= 2 {
		return result.Warn("Market timing is suboptimal — multiple warning signals"), nil
	}

	return result.Pass("Market timing conditions are acceptable"), nil
}
