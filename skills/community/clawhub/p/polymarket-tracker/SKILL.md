---
name: polymarket-tracker
description: Track top Polymarket markets by trading volume. Shows market name, Yes/No trading volumes, and current odds. Use when user asks about Polymarket trends, hot markets, or wants to find high-volume trading opportunities. Requires payment via skillpay.me (0.001 USDT per call).
---

# Polymarket Volume Tracker

Tracks real-time trading activity on Polymarket to identify high-volume markets.

## What It Does

Analyzes active Polymarket markets and returns:
- Market name
- Yes/No trading volumes
- Current odds (probability)
- Total volume ranking

## Usage

### Basic Usage
```bash
python scripts/track_volume.py --api-key YOUR_SKILLPAY_API_KEY --user-id YOUR_USER_ID
```

### Check Balance
```bash
python scripts/track_volume.py --api-key YOUR_SKILLPAY_API_KEY --user-id YOUR_USER_ID --check-balance
```

### Testing (Skip Payment)
```bash
python scripts/track_volume.py --api-key YOUR_KEY --skip-payment
```

### Environment Variables

You can also set credentials via environment variables:

```bash
export SKILLPAY_API_KEY=your_api_key_here
export SKILLPAY_USER_ID=your_user_id_here
python scripts/track_volume.py --api-key $SKILLPAY_API_KEY --user-id $SKILLPAY_USER_ID
```

## Payment Integration

This skill uses skillpay.me for payment:

- **Cost:** 0.001 USDT per call
- **API Key:** Get from skillpay.me Dashboard → Integration Config
- **Skill ID:** `ae30e94b-6cf4-444a-b734-f0ad65a50565`
- **Payment Method:** BNB Chain USDT
- **User ID:** Required for billing identification

### Payment Flow

1. **Check Balance:** System checks user's USDT balance
2. **Charge User:** If balance ≥ 0.001 USDT, deduct payment
3. **Insufficient Balance:** If balance < 0.001 USDT, returns payment link
4. **Top Up:** User can add balance via BNB Chain USDT payment link

## Output Format

Returns a formatted list of top 10 markets by volume:

```
============================================================
Top 10 Polymarket Markets (Last 10 Minutes)
============================================================

1. Market Name
   - Yes Volume: $X
   - No Volume: $Y
   - Yes Odds: Z%
   - No Odds: W%
   - Total Volume: $T

2. ...
```

## Data Source

- **API:** Polymarket Gamma API (`https://gamma-api.polymarket.com`)
- **Markets:** Active, non-closed markets only
- **Volume:** Total trading volume (lifetime)
- **Odds:** Current market odds from outcome prices

## Billing API Reference

This skill integrates with skillpay.me billing API:

### Check Balance
```python
balance = check_balance(user_id)
# Returns: float (USDT amount)
```

### Charge User
```python
result = charge_user(user_id, amount=0.001)
# Returns: {"success": bool, "balance": float, "payment_url": str (if failed)}
```

### Generate Payment Link
```python
url = get_payment_link(user_id, amount)
# Returns: str (BNB Chain USDT payment URL)
```

## Notes

- Volume data represents total market volume, not time-windowed
- Markets are sorted by total volume in descending order
- Returns top 10 markets with highest trading volume
- Payment required for each use (unless using `--skip-payment`)
- Minimum balance required: 0.001 USDT
