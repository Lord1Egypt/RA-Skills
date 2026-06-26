# Eligible Underlyings for PT Yield Strategy

This file defines which underlying assets are considered "stable-ish" and
eligible for the automated PT yield rollover strategy.

## Tier 1 — Major USD Stablecoins (lowest risk)

These are fully backed, audited, and have deep liquidity for USDC exit.

| Token   | Description                    | Notes |
|---------|--------------------------------|-------|
| USDC    | Circle USD                     | Native deposit token |
| USDT    | Tether USD                     | High liquidity |
| DAI     | MakerDAO stablecoin            | Overcollateralized |
| FRAX    | Frax stablecoin                | Partially algorithmic |
| PYUSD   | PayPal USD                     | Fiat-backed |
| GHO     | Aave GHO                       | Overcollateralized |

## Tier 2 — Yield-Bearing USD Stables (moderate risk)

These accrue yield and are redeemable for a Tier 1 stable, but carry
additional smart contract or protocol risk.

| Token    | Description                         | Underlying  | Notes |
|----------|-------------------------------------|-------------|-------|
| sDAI     | Spark DAI savings                   | DAI         | MakerDAO DSR |
| sFRAX    | Staked FRAX                         | FRAX        | Frax staking |
| sUSDe    | Staked USDe (Ethena)                | USDe        | Delta-neutral, newer |
| USDe     | Ethena USD                          | ETH hedged  | Synthetic stable |
| crvUSD   | Curve stablecoin                    | Multi-coll. | LLAMMA mechanism |
| USD0     | Usual Protocol                      | RWA-backed  | Newer entrant |
| USD0++   | Usual Protocol staked               | USD0        | Time-locked version |
| USDL     | Liquid USD (various)                | Varies      | Check specific issuer |

## Tier 3 — RWA / Tokenized Treasuries (moderate risk, different)

These represent real-world assets, typically US Treasury exposure.

| Token    | Description                         | Notes |
|----------|-------------------------------------|-------|
| USDY     | Ondo US Dollar Yield                | T-bill backed |
| BUIDL    | BlackRock USD Institutional Fund    | Tokenized MMF |
| OUSG     | Ondo Short-Term US Gov Bonds        | T-bill ETF tokenized |
| mUSD     | Mountain Protocol USD               | T-bill yield |
| wUSDM    | Wrapped Mountain USD                | Wrapped version |

## Tier 4 — Non-USD Stablecoins (opt-in only)

Only included when `include_non_usd=true`. These introduce FX risk.

| Token    | Peg  | Description                    | Notes |
|----------|------|--------------------------------|-------|
| EURS     | EUR  | Stasis Euro                    | Fiat-backed |
| EURA     | EUR  | Angle Euro (agEUR)             | Overcollateralized |
| agEUR    | EUR  | Angle Protocol Euro            | Same as EURA |
| XSGD     | SGD  | StraitsX Singapore Dollar      | Fiat-backed |
| EURe     | EUR  | Monerium Euro                  | Regulated e-money |

## Excluded — Never eligible

| Category       | Examples                              | Reason |
|----------------|---------------------------------------|--------|
| ETH-beta       | stETH, wstETH, rETH, cbETH, swETH    | Price risk to USD |
| BTC-beta       | WBTC, tBTC, cbBTC                     | Price risk to USD |
| Volatile DeFi  | PENDLE, CRV, AAVE, etc.              | Not stable |
| Points-only    | Markets with no real yield, just pts  | No economic return |
| Exotic vaults  | Leveraged vault tokens                | Complex risk |
| Unknown        | Any unrecognized underlying           | Requires manual review |

## How to update this list

When a new stablecoin or RWA token appears on Pendle:

1. Check what it's pegged to and how the peg is maintained
2. Check liquidity for swapping back to USDC
3. Check smart contract audit status
4. Assign to appropriate tier
5. Add to this file

The agent should flag any PT market whose underlying is NOT in this list
and ask the user before including it in the strategy.
