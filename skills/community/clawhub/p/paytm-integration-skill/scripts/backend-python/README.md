# Python backend (Flask) - Paytm reference

Reference Flask backend covering all four Paytm products in this skill: JS Checkout, Subscription (UPI Autopay), Payment Link, Dynamic QR.

Mirrors `scripts/backend-node` and `scripts/backend-spring` - same routes, same env vars.

## Setup

```bash
cd scripts/backend-python
pip install -r requirements.txt
```

## Run

```bash
PAYTM_MID="YOUR_MID" \
PAYTM_MERCHANT_KEY="YOUR_MERCHANT_KEY" \
PAYTM_WEBSITE_NAME="WEBSTAGING" \
python app.py
```

Demo pages:
- <http://localhost:5001/checkout.html> - one-time payment via JS Checkout
- <http://localhost:5001/subscription.html> - UPI Autopay subscription
- <http://localhost:5001/payment-link.html> - generate shareable payment link
- <http://localhost:5001/qr.html> - dynamic QR with auto-polling

See the repo-root `.env.example` for how to get your MID and Merchant Key.

## Env vars

| Var | Required | Default |
|---|---|---|
| `PAYTM_MID` | ✅ | none |
| `PAYTM_MERCHANT_KEY` | ✅ | none |
| `PAYTM_ENVIRONMENT` | optional | `staging` |
| `PAYTM_WEBSITE_NAME` | optional | `WEBSTAGING` (staging) / `DEFAULT` (production) |
| `PAYTM_CALLBACK_BASE` | optional | `http://localhost:5001` |
| `PAYTM_PG_DOMAIN` | optional | derived from `PAYTM_ENVIRONMENT` |
| `PAYTM_CALLBACK_URL` | optional | derived from `PAYTM_CALLBACK_BASE` |
| `PAYTM_STATUS_API_URL` | optional | `<pgDomain>/v3/order/status` |
| `PAYTM_CLIENT_ID` | optional | `C11` (per-merchant; override if your KAM gave you a different value) |
| `PORT` | optional | `5001` |

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/paytm-client-config.json` | mid + JS loader URL for the browser |
| POST | `/paytm/create-order` | initiateTransaction → `{orderId, txnToken, amount, mid}` (one-time payment) |
| POST | `/paytm/create-subscription` | `/subscription/create` → `{orderId, txnToken, subscriptionId, ...}` |
| POST | `/paytm/create-link` | `/link/create` → `{orderId, linkId, shortUrl, longUrl, ...}` |
| POST | `/paytm/link-transactions` | reconcile via `/link/fetchTransaction` → `{linkId, orders: [...]}` (use this for Payment Link flows, NOT `/v3/order/status`) |
| POST | `/paytm/create-qr` | `/paymentservices/qr/create` → `{orderId, qrCodeId, qrData, image, mid}` |
| POST | `/paytm/order-status` | server-side Transaction Status API |
| GET\|POST | `/paytm/callback` | Paytm browser redirect; verifies CHECKSUMHASH |

