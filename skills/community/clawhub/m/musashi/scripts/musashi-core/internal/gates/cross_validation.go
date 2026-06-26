package gates

import (
	"fmt"
	"math"
	"strconv"

	"github.com/yeheskieltame/musashi/scripts/musashi-core/internal/data"
)

// CrossValidationGate implements Gate 7: Cross-Validation.
// Compares DexScreener vs GeckoTerminal data for consistency.
type CrossValidationGate struct {
	dex   *data.DexScreenerClient
	gecko *data.GeckoTerminalClient
}

func NewCrossValidationGate() *CrossValidationGate {
	return &CrossValidationGate{
		dex:   data.NewDexScreenerClient(),
		gecko: data.NewGeckoTerminalClient(),
	}
}

func (g *CrossValidationGate) Name() string { return "Cross-Validation" }
func (g *CrossValidationGate) Number() int  { return 7 }

func (g *CrossValidationGate) Evaluate(token string, chainID int64) (*Result, error) {
	result := NewResult(g.Name(), g.Number())

	network := data.ChainIDToNetwork(chainID)

	// Fetch from both sources
	dexData, dexErr := g.dex.GetTokenPairs(token)
	geckoToken, geckoErr := g.gecko.GetToken(network, token)

	if dexErr != nil && geckoErr != nil {
		return result.Fail(fmt.Sprintf("Both data sources failed: dex=%v, gecko=%v", dexErr, geckoErr)), nil
	}

	// If only one source available, that's a yellow flag
	if dexErr != nil {
		result.AddEvidence("dexscreener", "error", dexErr.Error())
		return result.Warn("DexScreener unavailable — cannot cross-validate"), nil
	}
	if geckoErr != nil {
		result.AddEvidence("geckoterminal", "error", geckoErr.Error())
		return result.Warn("GeckoTerminal unavailable — cannot cross-validate"), nil
	}

	if len(dexData.Pairs) == 0 {
		return result.Fail("No DexScreener pairs for cross-validation"), nil
	}

	// Get best DexScreener pair
	var bestPair *data.DexPair
	for i := range dexData.Pairs {
		if bestPair == nil || dexData.Pairs[i].Liquidity.Usd > bestPair.Liquidity.Usd {
			bestPair = &dexData.Pairs[i]
		}
	}

	// Compare prices
	dexPrice, _ := strconv.ParseFloat(bestPair.PriceUsd, 64)
	geckoPrice, _ := strconv.ParseFloat(geckoToken.Attributes.PriceUsd, 64)

	result.AddEvidence("dexscreener", "price_usd", fmt.Sprintf("%.8f", dexPrice))
	result.AddEvidence("geckoterminal", "price_usd", fmt.Sprintf("%.8f", geckoPrice))

	if dexPrice > 0 && geckoPrice > 0 {
		priceDiff := math.Abs(dexPrice-geckoPrice) / ((dexPrice + geckoPrice) / 2) * 100
		result.AddEvidence("analysis", "price_divergence_pct", fmt.Sprintf("%.2f%%", priceDiff))

		if priceDiff > 10.0 {
			return result.Fail(fmt.Sprintf("Price divergence too high: %.1f%% between sources", priceDiff)), nil
		}
		if priceDiff > 5.0 {
			result.AddEvidence("analysis", "price_warning", "moderate price divergence")
		}
	}

	// Compare volumes
	dexVolume := bestPair.Volume.H24
	geckoVolume, _ := strconv.ParseFloat(geckoToken.Attributes.Volume24h, 64)

	result.AddEvidence("dexscreener", "volume_24h", fmt.Sprintf("%.2f", dexVolume))
	result.AddEvidence("geckoterminal", "volume_24h", fmt.Sprintf("%.2f", geckoVolume))

	if dexVolume > 0 && geckoVolume > 0 {
		volumeDiff := math.Abs(dexVolume-geckoVolume) / ((dexVolume + geckoVolume) / 2) * 100
		result.AddEvidence("analysis", "volume_divergence_pct", fmt.Sprintf("%.2f%%", volumeDiff))

		if volumeDiff > 50.0 {
			return result.Fail(fmt.Sprintf("Volume divergence suspicious: %.0f%% between sources", volumeDiff)), nil
		}
	}

	// Check pool distribution on GeckoTerminal
	geckoPools, err := g.gecko.GetTokenPools(network, token)
	if err == nil {
		result.AddEvidence("geckoterminal", "pool_count", fmt.Sprintf("%d", len(geckoPools)))

		if len(geckoPools) > 0 {
			result.AddEvidence("geckoterminal", "top_pool", geckoPools[0].Attributes.Name)
			result.AddEvidence("geckoterminal", "top_pool_reserve", geckoPools[0].Attributes.ReserveUsd)
		}
	}

	return result.Pass("Cross-validation consistent across data sources"), nil
}
