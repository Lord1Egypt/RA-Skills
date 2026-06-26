---
name: gtrade-with-cai
description: Trade gTrade perps via CAI — defi_markets, defi_preflight, defi_trade, defi_order_status, hosted /act enrollment. Requires platform or full API scope. Powered by CAI.com. Canonical skill v1.0.17.
metadata:
  version: 1.0.17
---

# gTrade with CAI (Route B)

CAI **E-mode** lets an agent trade **gTrade** perps using the custodial wallet after the user enables the platform at **`/automation-settings`** and completes **one** hosted enrollment on cai.com **`/act`**. Prefer unified **`defi_trade`** over legacy per-platform tools.

## When to Use

- "Trade gTrade with my CAI wallet"
- "Enable agent trading on Gains / gTrade"
- "Open a small BTC perp on Arbitrum or Polygon via CAI"
- "Check my gTrade order status after placing a trade"

## Route B task flow (preferred)

1. User enables **gtrade** at **`https://cai.com/automation-settings`** (browser; not API-key callable).
2. **`platform_readiness`** with `platform_slug=gtrade` (optional `chain`: `arbitrum` | `polygon`). If `ready_to_trade` is false, show `blocking_reasons` and stop.
3. If not enrolled: **`platform_automation_enroll`** with `platform_slug=gtrade` and `chain` → return **`url`**; user must complete **`/act`** (agent must **not** confirm for the user).
4. **Markets:** **`defi_markets`** with `platform_slug=gtrade` and `chain` — resolve `pair_index` from catalog.
5. **Preflight:** **`defi_preflight`** until `valid: true`.
6. **Place:** **`defi_trade`** with body example:
   - `platform_slug`: `gtrade`
   - `action`: `place`
   - `collateral_amount`, `pair_index`, `leverage`, `buy`, `chain`, `intent_usd`
7. **Status (primary):** poll **`defi_order_status`** with returned **`order_id`** until `is_terminal: true`.
8. **Status (secondary):** use **`defi_orders`** with `?platform_slug=gtrade&status=active` for resting orders; `status=terminal` for history.
9. **Close:** **`defi_trade`** with `action`: `close`, optional `trade_index` (omit when exactly one matching long), `symbol` / `pair_index`, `close_mode=full`, `chain`.
10. **Sell guard:** `place` + `buy=false` without long → preflight `NO_POSITION_TO_CLOSE` — use `action=close` instead.

## Legacy aliases (deprecated)

- `gtrade_open_trade` / `gtrade_close_trade` — do not use in new flows.

## Chain parameter

- **`chain`**: `arbitrum` (default) | `polygon`
- Enrollment may require **`enroll_approve`** per chain (`gtrade_arb_v1`, `gtrade_pol_v1`).

## Honesty

- **`gap_id`**: `GAP_DEFI_GTRADE_V1`, `GAP_DEFI_AUTOMATION_V1` — **`partial_live`** until enrollment + trade smokes pass in your environment.
- Server must include `gtrade` in **`DEFI_ENABLED_PLATFORMS`** and **`CUSTODIAL_DEFI_AUTOMATION_ENABLED=true`**.
- Do **not** use raw EVM calldata, generic sign-and-broadcast, or **`CAI_EVM_TX_PATH`**.

## Quick Setup

```bash
openclaw secrets set CAI_API_KEY "your_dashboard_api_key"
```

Scope: **`platform`** or **`full`**.

## Canonical Reference

- https://cai.com/skill.md §6.1b
- https://cai.com/specs/cai-tools.manifest.json
- https://cai.com/developers.html
