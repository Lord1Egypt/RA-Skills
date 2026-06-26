# Kamino Monitor – Reference

## Formulas

**Health ratio** = `borrowLiquidationLimit / totalBorrow`

**Health %** = `100 × (health - 1) / health`

**SOL liquidation price** = `P_now × (debt / (liquidationLtv × collateral))`

**Deposit for 60% health** = `2.5 × debt / liquidationLtv - collateral`

**Repay for same effect** = `debt - (collateral × liquidationLtv) / 2.5`

## Thresholds (wallets.json)

- `green` (default 1.6): health ratio for 🟢
- `yellow` (1.35): 🟡
- `orange` (1.2): 🟠
- Below orange: 🔴
