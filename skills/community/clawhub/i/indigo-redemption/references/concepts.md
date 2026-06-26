# Redemption & ROB Concepts

Key concepts for understanding the redemption system on the Indigo Protocol.

## Redemption Order Book (ROB)

The ROB is a mechanism that allows ADA holders to provide liquidity for iAsset redemptions. It acts as an order book where:

1. **Liquidity providers** deposit ADA and set a max price they're willing to pay for iAssets
2. **Redeemers** exchange iAssets for ADA at oracle price against these positions
3. **Providers** receive iAssets in return for their ADA

## ROB Order Book

The order book shows all open ROB positions, sorted by max price:

- **Lower max price** = earlier in the queue (filled first)
- **Higher max price** = later in the queue (filled last)
- Positions are filled sequentially from lowest to highest max price

## Redemption Queue

The redemption queue is an aggregated view of all ROB positions for an iAsset, showing total ADA available at each price level. It helps:

- Assess liquidity depth for redemptions
- Estimate fill times for new ROB positions
- Understand redemption pressure on an iAsset

## How Redemption Works

1. An iAsset holder calls `redeem_rob` with their iAssets
2. The protocol matches the redemption against ROB positions (lowest max price first)
3. The redeemer receives ADA at the oracle price
4. ROB providers receive iAssets in exchange for their ADA
5. A redemption fee is applied

## ROB Position Lifecycle

1. **Open** — Deposit ADA with a max price via `open_rob`
2. **Wait** — Position sits in the order book until filled by a redeemer
3. **Partially filled** — Some ADA exchanged for iAssets; position remains open
4. **Claim** — Call `claim_rob` to collect received iAssets
5. **Adjust** — Optionally add/remove ADA or change max price via `adjust_rob`
6. **Cancel** — Exit entirely and reclaim remaining ADA via `cancel_rob`

## Max Price

The max price is the highest price per iAsset unit that a ROB provider is willing to pay. For example:

- iUSD max price of 1.05 means the provider will pay up to 1.05 ADA per iUSD
- If oracle price > max price, the position won't be filled
- Lower max prices are filled first but may wait longer
