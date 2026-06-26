---
name: ostium-with-cai
description: Trade Ostium RWA perps on Arbitrum via CAI — defi_markets, defi_preflight, defi_trade, defi_order_status, hosted /act enrollment. Requires platform or full API scope. Powered by CAI.com. Canonical skill v1.0.17.
metadata:
  version: 1.0.17
---

# Ostium with CAI (Route B)

CAI **E-mode** lets an agent open and close **Ostium** RWA perpetuals on **Arbitrum** using the custodial wallet. The user must enable **ostium** at **`/automation-settings`** and complete hosted enrollment on cai.com **`/act`**. No separate Ostium website signup is required for CAI-managed trading.

## When to Use

- "Trade Ostium with my CAI wallet"
- "Open an Ostium RWA perp on Arbitrum"
- "Enable Ostium automation for my agent"
- "Check Ostium order status after my trade"

## Route B task flow (preferred)

1. User enables **ostium** at **`https://cai.com/automation-settings`**.
2. **`platform_readiness`** with `platform_slug=ostium`. If `ready_to_trade` is false, read `blocking_reasons` (e.g. `OSTIUM_APPROVE_REQUIRED`) and guide the user.
3. If not enrolled: **`platform_automation_enroll`** with `platform_slug=ostium` → user opens **`url`** on **`/act`** and confirms USDC approve (`ostium_arb_v1`).
4. Ensure custodial **Arbitrum USDC** (+ gas) via **`wallet_balances`** or deposit flows if needed.
5. **Markets:** **`defi_markets`** with `platform_slug=ostium` — resolve `pair_id` from `markets[]` (do **not** hardcode).
6. **Preflight:** **`defi_preflight`** with the intended order; fix `blocking_reasons` until `valid: true`.
7. **Place:** **`defi_trade`** example body:
   - `platform_slug`: `ostium`
   - `action`: `place`
   - `collateral_amount`, `pair_id`, `leverage`, `buy`, `price`, `order_type`, `intent_usd`
8. **Status (primary):** poll **`defi_order_status`** with returned **`order_id`** until `is_terminal: true`.
9. **Status (secondary):** **`defi_orders`** with `?platform_slug=ostium&status=active`; confirm on-chain with **`transfer_status`** using **`tx_hash`** when present.
10. **Close:** **`defi_trade`** with `action`: `close`, optional `trade_index` (omit when exactly one matching long), `symbol` / `pair_id`, `close_mode=full`.
11. **Sell guard:** `place` + `buy=false` without long → preflight `NO_POSITION_TO_CLOSE` — use `action=close` instead.

## Legacy aliases (deprecated)

- `ostium_open_trade` / `ostium_close_trade` — do not use in new flows.

## Honesty

- **`gap_id`**: `GAP_DEFI_OSTIUM_V1`, `GAP_DEFI_AUTOMATION_V1` — **`partial_live`** until staging/production smokes pass.
- **`ostium`** must be in server **`DEFI_ENABLED_PLATFORMS`**.
- v1 uses **Self+Self** EVM signing only (no gasless delegate in v1).
- Do **not** expose raw calldata or generic wallet signing.

## Quick Setup

```bash
openclaw secrets set CAI_API_KEY "your_dashboard_api_key"
```

Scope: **`platform`** or **`full`**.

## Canonical Reference

- https://cai.com/skill.md §6.1b
- https://cai.com/specs/cai-tools.manifest.json
- https://cai.com/developers.html
