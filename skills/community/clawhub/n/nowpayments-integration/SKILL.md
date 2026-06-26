# NowPayments Integration Skill
## Accept crypto payments in your AI agent's store

### What It Does
Sets up NowPayments cryptocurrency payment processing for AI-operated stores:
- Payment API integration
- IPN callback handling
- Multi-currency support (200+ coins)
- Auto-payment verification
- Order status tracking

### Prerequisites
- NowPayments account (free at nowpayments.io)
- API key from NowPayments dashboard
- IPN secret from Store Settings → IPN

### Setup Instructions
Tell your AI: "Set up NowPayments for my store."

Your AI will:
1. Create `.env` with NOWPAYMENTS_API_KEY and NOWPAYMENTS_IPN_SECRET
2. Create `/api/checkout` endpoint with:
   - Product validation
   - Payment creation
   - Rate limiting (10 req/min per IP)
   - CSRF protection
3. Create `/api/payment-callback` for IPN webhooks
4. Wire the checkout button to call the API
5. Add payment status polling to the success page

### Products Configuration
```javascript
const PRODUCTS = {
  blueprint: { name: "Product Name", price: 29, desc: "Description" },
  kit: { name: "Product Name", price: 97, desc: "Description" },
  // Add more products as needed
}
```

### Security Features
- Origin header validation (CSRF defense)
- Content-Type enforcement
- Rate limiting per IP
- No API key in client-side code
- IPN signature verification

### Testing
```bash
curl -X POST http://localhost:3000/api/checkout \
  -H "Content-Type: application/json" \
  -d '{"productId": "blueprint"}'
```

Response includes:
- `payment_id` — NowPayments ID
- `pay_address` — Crypto wallet address
- `pay_amount` — Amount in crypto
- `pay_currency` — Currency (default: usdterc20)

### Version
1.0 by TalonForge

### Links
- Store example: https://www.talonforge.xyz/store
- NowPayments docs: https://documenter.getpostman.com/view/7900902/S1a7UnNT