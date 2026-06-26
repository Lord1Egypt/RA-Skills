---
name: Hype
description: Assist with Hyperliquid perpetuals trading, deposits, withdrawals, and L1 features.
metadata: {"clawdbot":{"emoji":"🟢","os":["linux","darwin","win32"]}}
---

## Deposits and Withdrawals
- Deposits only via Arbitrum — bridge USDC from Arbitrum to Hyperliquid
- Native USDC only — not USDC.e or other bridged versions
- Withdrawals back to Arbitrum — same bridge, takes a few minutes
- No direct deposits from Ethereum mainnet — must bridge to Arbitrum first
- Minimum deposit/withdrawal amounts apply — check current limits

## Account Model
- Single margin account — all positions share collateral
- Cross-margin by default — profits from one position offset losses in another
- Isolated margin available per position — limits risk but reduces capital efficiency
- Account value = deposits + unrealized PnL — real-time calculation

## Trading Perpetuals
- Perpetual futures with up to 50x leverage — higher leverage = higher liquidation risk
- Funding rates every hour — longs pay shorts or vice versa based on price vs index
- Mark price for liquidations — not last traded price, reduces manipulation
- Order types: limit, market, stop-loss, take-profit, trailing stop
- Reduce-only orders to close without accidentally increasing position

## Liquidations
- Liquidation price visible before opening position — calculate carefully with leverage
- Partial liquidations happen first — position reduced before full liquidation
- Insurance fund covers bad debt — but don't rely on it
- Cross-margin means other positions' profits protect you — but losses can cascade
- ADL (Auto-Deleveraging) in extreme cases — profitable traders may be force-closed

## Order Execution
- On-chain order book — fully decentralized, verifiable
- Sub-second block times — near-instant execution
- No gas fees for trading — fees are trading fees only
- API available for programmatic trading — rate limits apply
- Cancellations are instant — no pending cancel state

## Vaults and Staking
- HLP (Hyperliquid Provider) vault — earn fees from market making
- Deposit USDC to earn yield — but exposed to vault performance
- Vault performance varies — can be negative during high volatility
- Staking HYPE token for governance — separate from trading

## HYPE Token
- Native token of Hyperliquid L1 — used for gas on the L1 chain
- Airdrop distributed to early users — based on trading volume and points
- Staking for chain security — validators run on HYPE stake
- Trading fees partially go to HYPE stakers — revenue sharing model

## Risk Management
- Set stop-losses before entering positions — discipline prevents disasters
- Monitor funding rates — paying high funding erodes profits
- Check open interest and liquidity — low liquidity means higher slippage
- Avoid max leverage — leaves no room for price movement
- Understand cross-margin implications — one bad trade can affect all positions

## API and Automation
- REST and WebSocket APIs available — full trading functionality
- Rate limits per IP and account — respect limits to avoid bans
- Testnet available — practice without real funds
- SDK in Python — official and community libraries exist

## Common Issues
- "Insufficient margin" — need more USDC or reduce position size
- "Order would trigger liquidation" — leverage too high for position size
- "Rate limited" — slow down API requests
- Withdrawal delayed — network congestion, usually resolves quickly
- Position not showing — refresh or check subaccounts

## Security
- Non-custodial — funds secured by your wallet
- Connect via wallet signature — no deposits to exchange address
- Revoke connections when done — permissions persist until revoked
- Verify site URL — phishing sites common for DEXs
- No KYC required — but geo-restrictions may apply
