package gates

import (
	"fmt"
	"strconv"

	"github.com/yeheskieltame/musashi/scripts/musashi-core/internal/data"
)

// WalletsGate implements Gate 3: Wallet Behavior.
// Uses DexScreener transaction data + GoPlus holder info.
type WalletsGate struct {
	dex    *data.DexScreenerClient
	goplus *data.GoPlusClient
}

func NewWalletsGate() *WalletsGate {
	return &WalletsGate{
		dex:    data.NewDexScreenerClient(),
		goplus: data.NewGoPlusClient(),
	}
}

func (g *WalletsGate) Name() string { return "Wallet Behavior" }
func (g *WalletsGate) Number() int  { return 3 }

func (g *WalletsGate) Evaluate(token string, chainID int64) (*Result, error) {
	result := NewResult(g.Name(), g.Number())

	// GoPlus holder data
	sec, err := g.goplus.GetTokenSecurity(chainID, token)
	if err != nil {
		return result.Fail(fmt.Sprintf("GoPlus API error: %v", err)), nil
	}

	result.AddEvidence("goplus", "holder_count", sec.HolderCount)
	result.AddEvidence("goplus", "creator_address", sec.CreatorAddress)

	// Check 1: Minimum holders
	holderCount, _ := strconv.Atoi(sec.HolderCount)
	if holderCount < 50 {
		return result.Fail(fmt.Sprintf("Too few holders: %d (min 50)", holderCount)), nil
	}

	// DexScreener transaction data for buy/sell analysis
	dexData, err := g.dex.GetTokenPairs(token)
	if err != nil {
		return result.Fail(fmt.Sprintf("DexScreener API error: %v", err)), nil
	}

	if len(dexData.Pairs) == 0 {
		return result.Fail("No trading pairs found"), nil
	}

	// Aggregate buy/sell across all pairs
	var totalBuys, totalSells int
	for _, p := range dexData.Pairs {
		totalBuys += p.Txns.H24.Buys
		totalSells += p.Txns.H24.Sells
	}

	result.AddEvidence("dexscreener", "buys_24h", fmt.Sprintf("%d", totalBuys))
	result.AddEvidence("dexscreener", "sells_24h", fmt.Sprintf("%d", totalSells))

	totalTxns := totalBuys + totalSells
	if totalTxns == 0 {
		return result.Fail("No transactions in 24h — dead token"), nil
	}

	sellRatio := float64(totalSells) / float64(totalTxns)
	result.AddEvidence("analysis", "sell_ratio", fmt.Sprintf("%.2f", sellRatio))

	// Check 2: Sustained sell pressure
	if sellRatio > 0.70 {
		return result.Fail(fmt.Sprintf("Heavy sell pressure: %.0f%% sells in 24h", sellRatio*100)), nil
	}

	// Check 3: Transaction count sanity
	if totalTxns < 20 {
		result.AddEvidence("analysis", "low_activity", "true")
		return result.Fail(fmt.Sprintf("Very low activity: only %d transactions in 24h", totalTxns)), nil
	}

	// Check 4: Buy/sell balance across timeframes
	var bestPair *data.DexPair
	for i := range dexData.Pairs {
		if bestPair == nil || dexData.Pairs[i].Liquidity.Usd > bestPair.Liquidity.Usd {
			bestPair = &dexData.Pairs[i]
		}
	}

	if bestPair != nil {
		h1Buys := bestPair.Txns.H1.Buys
		h1Sells := bestPair.Txns.H1.Sells
		result.AddEvidence("dexscreener", "buys_1h", fmt.Sprintf("%d", h1Buys))
		result.AddEvidence("dexscreener", "sells_1h", fmt.Sprintf("%d", h1Sells))

		// Short-term sell dump detection
		h1Total := h1Buys + h1Sells
		if h1Total > 10 {
			h1SellRatio := float64(h1Sells) / float64(h1Total)
			if h1SellRatio > 0.80 {
				return result.Fail(fmt.Sprintf("Active dump: %.0f%% sells in last hour", h1SellRatio*100)), nil
			}
		}
	}

	return result.Pass("Wallet behavior is healthy"), nil
}
