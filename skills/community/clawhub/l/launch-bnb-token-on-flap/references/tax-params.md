# Tax Token Parameters

Collect each parameter below from the user. Validate constraints before proceeding.

## Rates (basis points, 1% = 100 bps)

| Parameter | Type | Constraints | Default / Suggestion |
|---|---|---|---|
| `buyTaxRate` | `uint16` | 0–1000 (0%–10%) | 300 (3%) |
| `sellTaxRate` | `uint16` | 0–1000 (0%–10%) | 1000 (10%) |

Asymmetric buy/sell rates are supported (Tax Token V3). One rate can be zero, but not both. 

## Durations

| Parameter | Type | Constraints | Default |
|---|---|---|---|
| `taxDuration` | `uint64` seconds | min 365 days; max 100 years | `100 * 365 days` |
| `antiFarmerDuration` | `uint64` seconds | min 1 day; max 1 year | `3 days` |

`taxDuration` is how long the tax is applied. After it expires the token behaves like a standard token.
`antiFarmerDuration` prevents farmers from draining the trading fees.  

## Revenue distribution (must sum to exactly 10 000)

| Parameter | Description |
|---|---|
| `mktBps` | Basis points sent to the `beneficiary` (or vault). Must be > 0 if using a Vault Factory |
| `deflationBps` | Basis points burned. |
| `dividendBps` | Basis points routed to the dividend contract. |
| `lpBps` | Basis points added as LP (sent to dead address). |

**Constraint:** `mktBps + deflationBps + dividendBps + lpBps == 10000`

Typical simple configuration: `mktBps = 10000`, all others = 0.

## Other fields

| Parameter | Type | Notes |
|---|---|---|
| `minimumShareBalance` | `uint256` | Minimum token balance required to be eligible for dividends. Set `0` if `dividendBps == 0`. |
| `beneficiary` | `address` | Address that receives `mktBps` revenue. **Only for tax token without vault.** When using a vault, the vault contract is set automatically as beneficiary. |

## Summary checklist

Before proceeding, confirm:
- [ ] At least one of `buyTaxRate` or `sellTaxRate` must be non-zero. Neither rate may exceed 1000 (10%). 
- [ ] `taxDuration >= 365 days` (31 536 000 seconds).
- [ ] `antiFarmerDuration >= 1 day` (86 400 seconds).
- [ ] `mktBps + deflationBps + dividendBps + lpBps == 10000`.
- [ ] `mktBps > 0` if using a Vault Factory.
- [ ] `beneficiary` must be non-zero address, by default set to your EVM address if launching a tax token without vault. 
