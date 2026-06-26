---
name: hyperliquid-with-cai
description: Trade Hyperliquid perps via CAI — defi_markets, defi_preflight, defi_trade, defi_order_status, no HL website signup. Requires platform or full API scope. Powered by CAI.com. Canonical skill v1.0.17.
metadata:
  version: 1.0.17
---

# Hyperliquid with CAI (Route B)

CAI **E-mode** trades **Hyperliquid** perpetuals using a **custodial EVM address** and a **derived agent key**. The user does **not** register on hyperliquid.xyz. Protocol onboarding is **`approveAgent`** (and optional deposit) via hosted **`/act`**, not a separate HL account.

## When to Use

- "Trade Hyperliquid perps with my CAI wallet"
- "Enable HL agent trading without creating a Hyperliquid account"
- "Place a small BTC perp on Hyperliquid after enrollment"
- "Show my HL open orders and positions"

## Route B task flow (preferred)

1. User enables **hyperliquid** at **`https://cai.com/automation-settings`**.
2. **`platform_readiness`** or **`defi_portfolio`** with `platform_slug=hyperliquid`. If `deposit_required`, guide user through **`/act`** with optional **`hl_deposit_usd`** or explain bridge timing (~1 min after ARB USDC bridge).
3. If not enrolled: **`platform_automation_enroll`** with `platform_slug=hyperliquid` → user completes **`/act`** (`approveAgent`).
4. **Markets:** **`defi_markets`** with `platform_slug=hyperliquid` and optional `dex` — resolve `asset` from catalog.
5. **Preflight:** **`defi_preflight`** until `valid: true`.
6. **Place:** **`defi_trade`** example:
   - `platform_slug`: `hyperliquid`
   - `action`: `place`
   - `asset`: `BTC` (or HIP-3 `xyz:SYMBOL`)
   - `size`, `price`, `is_buy`, `intent_usd`, optional `dex`
7. **Status (primary):** poll **`defi_order_status`** with returned canonical **`order_id`** until `is_terminal: true`.
8. **Status (secondary):** **`defi_orders`** (`?status=active`) and **`defi_positions`** with `?platform_slug=hyperliquid`.
9. **Close:** **`defi_trade`** with `action`: `close`, `asset`, `close_mode=full` (or `intent_usd=max`) — reduce-only; no `trade_index`.
10. **Cancel:** **`defi_trade`** with `action`: `cancel`, `oid` + `asset` (or `cancels[]`).
11. **Sell guard:** `place` + `is_buy=false` without long → preflight `NO_POSITION_TO_CLOSE` — use `action=close` instead.

## Legacy aliases (deprecated)

- `hyperliquid_readiness`, `hyperliquid_place_order`, `hyperliquid_cancel`, `hyperliquid_positions` — do not use in new flows.

## What NOT to say

- Do **not** tell users to "register on Hyperliquid" or "login to hyperliquid.xyz".
- Do **not** use **`transfer_status`** for HL order lifecycle (use **`defi_orders`**).

## Honesty

- **`gap_id`**: `GAP_DEFI_HYPERLIQUID_V1`, `GAP_DEFI_AUTOMATION_V1` — **`partial_live`** until enroll + trade smokes pass.
- Agent key cannot withdraw to arbitrary addresses (protocol design).
- HIP-3 / trade.xyz markets: use `asset` like `xyz:NVDA` or `dex` param — see trade-xyz-with-cai wrapper for narrative.

## Quick Setup

```bash
openclaw secrets set CAI_API_KEY "your_dashboard_api_key"
```

Scope: **`platform`** or **`full`**.

## Canonical Reference

- https://cai.com/skill.md §6.1b
- https://cai.com/specs/cai-tools.manifest.json
- https://cai.com/developers.html
