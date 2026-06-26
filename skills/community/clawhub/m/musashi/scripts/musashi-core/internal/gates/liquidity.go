package gates

import (
	"fmt"

	"github.com/yeheskieltame/musashi/scripts/musashi-core/internal/data"
)

// LiquidityGate implements Gate 2: Liquidity Structure.
// Uses DexScreener + GoPlus LP data.
type LiquidityGate struct {
	dex    *data.DexScreenerClient
	goplus *data.GoPlusClient
}

func NewLiquidityGate() *LiquidityGate {
	return &LiquidityGate{
		dex:    data.NewDexScreenerClient(),
		goplus: data.NewGoPlusClient(),
	}
}

func (g *LiquidityGate) Name() string { return "Liquidity Structure" }
func (g *LiquidityGate) Number() int  { return 2 }

func (g *LiquidityGate) Evaluate(token string, chainID int64) (*Result, error) {
	result := NewResult(g.Name(), g.Number())

	// Fetch DexScreener data
	dexData, err := g.dex.GetTokenPairs(token)
	if err != nil {
		return result.Fail(fmt.Sprintf("DexScreener API error: %v", err)), nil
	}

	if len(dexData.Pairs) == 0 {
		return result.Fail("No trading pairs found — token not listed on any DEX"), nil
	}

	// Use the highest-liquidity pair as primary
	var bestPair *data.DexPair
	for i := range dexData.Pairs {
		if bestPair == nil || dexData.Pairs[i].Liquidity.Usd > bestPair.Liquidity.Usd {
			bestPair = &dexData.Pairs[i]
		}
	}

	totalLiquidity := 0.0
	for _, p := range dexData.Pairs {
		totalLiquidity += p.Liquidity.Usd
	}

	result.AddEvidence("dexscreener", "total_liquidity_usd", fmt.Sprintf("%.2f", totalLiquidity))
	result.AddEvidence("dexscreener", "best_pair_dex", bestPair.DexID)
	result.AddEvidence("dexscreener", "best_pair_liquidity", fmt.Sprintf("%.2f", bestPair.Liquidity.Usd))
	result.AddEvidence("dexscreener", "pair_count", fmt.Sprintf("%d", len(dexData.Pairs)))
	result.AddEvidence("dexscreener", "fdv", fmt.Sprintf("%.2f", bestPair.FDV))
	result.AddEvidence("dexscreener", "market_cap", fmt.Sprintf("%.2f", bestPair.MarketCap))
	result.AddEvidence("dexscreener", "price_usd", bestPair.PriceUsd)
	result.AddEvidence("dexscreener", "volume_24h", fmt.Sprintf("%.2f", bestPair.Volume.H24))

	// Check 1: Minimum liquidity
	if totalLiquidity < 10000 {
		return result.Fail(fmt.Sprintf("Total liquidity too low: $%.0f (min $10,000)", totalLiquidity)), nil
	}

	// Check 2: LP depth vs market cap
	// For tokens with >$1M DEX liquidity, ratio is less relevant (they likely trade on CEX too)
	// For smaller tokens, ratio is critical — thin LP = easy rug
	if bestPair.MarketCap > 0 {
		lpRatio := totalLiquidity / bestPair.MarketCap
		result.AddEvidence("dexscreener", "lp_to_mcap_ratio", fmt.Sprintf("%.4f", lpRatio))

		if lpRatio < 0.05 {
			if totalLiquidity >= 1000000 {
				// >$1M absolute liquidity — ratio is low but real liquidity exists (likely CEX-listed)
				result.AddEvidence("analysis", "lp_context", fmt.Sprintf("LP ratio %.1f%% is low but absolute liquidity $%.0fM is substantial — likely CEX-listed token", lpRatio*100, totalLiquidity/1000000))
			} else {
				return result.Fail(fmt.Sprintf("LP depth too thin: %.1f%% of market cap (min 5%%)", lpRatio*100)), nil
			}
		}
	}

	// Check 3: Liquidity concentration
	if bestPair.Liquidity.Usd/totalLiquidity > 0.95 && len(dexData.Pairs) > 1 {
		result.AddEvidence("analysis", "liquidity_concentration", fmt.Sprintf("%.1f%% on %s", bestPair.Liquidity.Usd/totalLiquidity*100, bestPair.DexID))
		// Warning but not instant fail if only one DEX
	}

	// Check 4: GoPlus LP lock status
	sec, err := g.goplus.GetTokenSecurity(chainID, token)
	if err == nil && len(sec.LPHolders) > 0 {
		totalLPLocked := 0
		for _, lp := range sec.LPHolders {
			if lp.IsLocked == 1 {
				totalLPLocked++
			}
		}
		result.AddEvidence("goplus", "lp_holders", fmt.Sprintf("%d", len(sec.LPHolders)))
		result.AddEvidence("goplus", "lp_locked_count", fmt.Sprintf("%d", totalLPLocked))

		if totalLPLocked == 0 && len(sec.LPHolders) > 0 {
			return result.Fail("No LP is locked — rug pull risk"), nil
		}
	}

	// Check 5: Volume sanity
	if bestPair.Volume.H24 < 1000 {
		return result.Fail(fmt.Sprintf("24h volume too low: $%.0f", bestPair.Volume.H24)), nil
	}

	return result.Pass("Liquidity structure is healthy"), nil
}
