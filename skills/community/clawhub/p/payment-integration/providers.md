# Payment Provider Detailed Reference

## 1. Stripe

**API Model**: RESTful, versioned (e.g. `2024-12-18.acacia`). Client libraries handle versioning.
**Auth**: Secret key (`sk_test_...` / `sk_live_...`) as Bearer token.
**Base URL**: `https://api.stripe.com/v1`

### Core Flow — PaymentIntents (recommended)

```typescript
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

// Server: Create PaymentIntent
const paymentIntent = await stripe.paymentIntents.create({
  amount: 2000, // $20.00 in cents
  currency: 'usd',
  automatic_payment_methods: { enabled: true },
  idempotency_key: orderId, // CRITICAL: prevents duplicate charges
});
// Send paymentIntent.client_secret to frontend

// Frontend: Confirm with Stripe.js
const { error } = await stripe.confirmPayment({
  elements,
  confirmParams: { return_url: 'https://example.com/success' },
});
```

### Checkout Sessions (hosted page)

```typescript
const session = await stripe.checkout.sessions.create({
  line_items: [{ price: 'price_xxx', quantity: 1 }],
  mode: 'payment',
  success_url: 'https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
  cancel_url: 'https://example.com/cancel',
});
// Redirect user to session.url
```

### Webhook Verification (CRITICAL — must use raw body)

```typescript
import { buffer } from 'node:stream/consumers';

app.post('/webhook', async (req, res) => {
  const rawBody = await buffer(req); // Must be raw, NOT parsed JSON
  const sig = req.headers['stripe-signature']!;

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(rawBody, sig, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch (err) {
    console.error('Webhook signature verification failed');
    return res.status(400).send('Invalid signature');
  }

  switch (event.type) {
    case 'payment_intent.succeeded':
      const pi = event.data.object as Stripe.PaymentIntent;
      await fulfillOrder(pi.metadata.orderId);
      break;
    case 'payment_intent.payment_failed':
      // Handle failure
      break;
  }

  res.json({ received: true }); // Return 200 fast
});
```

### Common Pitfalls

- Using the deprecated Charges API instead of PaymentIntents
- Parsing the request body before passing to `constructEvent` — signature verification WILL fail
- Not using idempotency keys — can result in duplicate charges on retries
- Hardcoding API keys instead of using environment variables
- Not handling `requires_action` status (3D Secure)

**Test Cards**: `4242424242424242` (success), `4000000000009995` (decline), `4000002500003155` (3DS required)

---

## 2. PayPal

**API Model**: REST v2, OAuth2 client credentials.
**Auth**: Base64-encode `client_id:client_secret`, exchange for Bearer token.
**Base URL**: `https://api-m.sandbox.paypal.com` (sandbox) / `https://api-m.paypal.com` (live)

### Core Flow — Orders API v2

```typescript
// Step 1: Get access token
const auth = Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString('base64');
const tokenRes = await fetch('https://api-m.sandbox.paypal.com/v1/oauth2/token', {
  method: 'POST',
  headers: {
    'Authorization': `Basic ${auth}`,
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: 'grant_type=client_credentials',
});
const { access_token } = await tokenRes.json();

// Step 2: Create order
const orderRes = await fetch('https://api-m.sandbox.paypal.com/v2/checkout/orders', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    intent: 'CAPTURE',
    purchase_units: [{
      amount: { currency_code: 'USD', value: '20.00' },
    }],
  }),
});
const order = await orderRes.json();
// Redirect user to order.links.find(l => l.rel === 'approve').href

// Step 3: Capture after user approves
const captureRes = await fetch(
  `https://api-m.sandbox.paypal.com/v2/checkout/orders/${orderId}/capture`,
  {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${access_token}`, 'Content-Type': 'application/json' },
  }
);
```

### Common Pitfalls

- Webhook events may arrive OUT OF ORDER — don't assume APPROVED comes before COMPLETED
- OAuth tokens expire (typically 9 hours) — cache and refresh
- Sandbox and live use different base URLs — use env vars
- `PENDING` capture status is normal for eCheck payments — don't treat as failure
- Always verify webhook signatures — PayPal uses a certificate chain

**Test Account**: Create sandbox buyer/seller accounts at developer.paypal.com

---

## 3. Alipay (支付宝)

**API Model**: OpenAPI 2.0, RSA2 (SHA256withRSA) signature auth.
**Auth**: App ID + private key signing. Every request is signed.
**Base URL**: `https://openapi.alipay.com/gateway.do` (live) / `https://openapi-sandbox.dl.alipaydev.com/gateway.do` (sandbox)

### Core Flow — Website Payment (电脑网站支付)

```typescript
import crypto from 'node:crypto';

function signParams(params: Record<string, string>, privateKey: string): string {
  const sortedKeys = Object.keys(params).filter(k => params[k] !== '' && k !== 'sign').sort();
  const signStr = sortedKeys.map(k => `${k}=${params[k]}`).join('&');
  const sign = crypto.createSign('RSA-SHA256');
  sign.update(signStr, 'utf8');
  return sign.sign(privateKey, 'base64');
}

const params: Record<string, string> = {
  app_id: process.env.ALIPAY_APP_ID!,
  method: 'alipay.trade.page.pay',
  charset: 'utf-8',
  sign_type: 'RSA2',
  timestamp: new Date().toISOString().replace('T', ' ').slice(0, 19),
  version: '1.0',
  notify_url: 'https://example.com/alipay/notify', // Async callback
  return_url: 'https://example.com/alipay/return',  // Sync redirect
  biz_content: JSON.stringify({
    out_trade_no: orderId,
    total_amount: '20.00',
    subject: 'Order Payment',
    product_code: 'FAST_INSTANT_TRADE_PAY',
  }),
};
params.sign = signParams(params, privateKey);
// Build form and auto-submit to Alipay gateway
```

### Webhook (异步通知) Verification

```typescript
function verifyAlipayNotify(params: Record<string, string>, alipayPublicKey: string): boolean {
  const sign = params.sign;
  const signType = params.sign_type;
  const sortedKeys = Object.keys(params)
    .filter(k => k !== 'sign' && k !== 'sign_type' && params[k] !== '')
    .sort();
  const signStr = sortedKeys.map(k => `${k}=${params[k]}`).join('&');

  const verify = crypto.createVerify('RSA-SHA256');
  verify.update(signStr, 'utf8');
  return verify.verify(alipayPublicKey, sign, 'base64');
}
// Return "success" string (not JSON!) to acknowledge
```

### Common Pitfalls

- `notify_url` (async webhook) vs `return_url` (user redirect) — NEVER rely on return_url for order fulfillment, it may not be called
- Charset MUST be `utf-8` — mismatches cause signature verification failure
- RSA2 (SHA256) is required — RSA (SHA1) is deprecated
- Response to notify must be the plain string `success` — not JSON, not HTML
- China business license required for real merchant account
- Amount is a string with 2 decimal places, not an integer

---

## 4. WeChat Pay (微信支付)

**API Model**: REST V3 (JSON), RSA-SHA256 signature auth + platform certificates.
**Auth**: Merchant ID + API v3 key + merchant certificate (serial number + private key).
**Base URL**: `https://api.mch.weixin.qq.com/v3`

### V3 Signature Construction

```typescript
import crypto from 'node:crypto';

function buildAuthHeader(
  method: string, url: string, body: string,
  merchantId: string, serialNo: string, privateKey: string
): string {
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const nonce = crypto.randomBytes(16).toString('hex');
  const message = `${method}\n${url}\n${timestamp}\n${nonce}\n${body}\n`;

  const sign = crypto.createSign('RSA-SHA256');
  sign.update(message);
  const signature = sign.sign(privateKey, 'base64');

  return `WECHATPAY2-SHA256-RSA2048 mchid="${merchantId}",nonce_str="${nonce}",timestamp="${timestamp}",serial_no="${serialNo}",signature="${signature}"`;
}

// Native Payment (QR code)
const url = '/v3/pay/transactions/native';
const body = JSON.stringify({
  appid: process.env.WECHAT_APP_ID,
  mchid: process.env.WECHAT_MCH_ID,
  description: 'Order Payment',
  out_trade_no: orderId,
  notify_url: 'https://example.com/wechat/notify',
  amount: { total: 2000, currency: 'CNY' }, // Amount in fen (分)
});

const res = await fetch(`https://api.mch.weixin.qq.com${url}`, {
  method: 'POST',
  headers: {
    'Authorization': buildAuthHeader('POST', url, body, merchantId, serialNo, privateKey),
    'Content-Type': 'application/json',
  },
  body,
});
const { code_url } = await res.json(); // QR code URL
```

### Webhook Decryption (AES-256-GCM)

```typescript
function decryptWechatNotify(
  ciphertext: string, nonce: string, associatedData: string, apiV3Key: string
): string {
  const decipher = crypto.createDecipheriv(
    'aes-256-gcm',
    Buffer.from(apiV3Key), // Must be exactly 32 bytes
    Buffer.from(nonce),
  );
  decipher.setAAD(Buffer.from(associatedData));

  const encrypted = Buffer.from(ciphertext, 'base64');
  const authTag = encrypted.subarray(-16);
  const data = encrypted.subarray(0, -16);

  decipher.setAuthTag(authTag);
  const decrypted = Buffer.concat([decipher.update(data), decipher.final()]);
  return decrypted.toString('utf8');
}
```

### Common Pitfalls

- V2 (XML) vs V3 (JSON) API — always use V3 for new integrations
- Amount in **fen** (分), not yuan (元) — 1 yuan = 100 fen
- JSAPI payment requires user's `openid` — must do OAuth2 first
- Platform certificate rotation — download and cache certificates, check serial number
- The API v3 key (for webhook decryption) is DIFFERENT from the API key (for signing)
- Webhook body is encrypted, not just signed — must decrypt before processing

---

## 5. Apple Pay

**Integration Model**: Apple Pay is a payment METHOD, not a processor. You still need a payment processor (Stripe, PayPal, etc.) to actually charge the card.

### Recommended: Via Stripe

```typescript
// Stripe handles Apple Pay automatically with PaymentIntents
// Just enable Apple Pay in Stripe Dashboard → Payment Methods
// And verify your domain

// Frontend (Stripe.js)
const paymentRequest = stripe.paymentRequest({
  country: 'US',
  currency: 'usd',
  total: { label: 'Order Total', amount: 2000 },
  requestPayerName: true,
  requestPayerEmail: true,
});

// Check if Apple Pay is available
const result = await paymentRequest.canMakePayment();
if (result?.applePay) {
  // Show Apple Pay button
}
```

### Direct Integration Requirements

1. Apple Developer Account ($99/year)
2. Merchant ID registration
3. Payment Processing Certificate (uploaded to your processor)
4. Merchant Identity Certificate (for server-side session creation)
5. Domain Verification: host `apple-developer-merchantid-domain-association` file at `/.well-known/`

### Common Pitfalls

- Domain verification file must be served over HTTPS without redirects
- Merchant session must be created server-side (not from browser)
- Testing requires a real Apple device with a card in Wallet
- Safari-only on web (or via Stripe/PayPal JS which handle this)

---

## 6. Google Pay

**Integration Model**: Like Apple Pay, Google Pay is a payment method. You need a processor.

### Via Stripe (recommended)

```typescript
// Stripe.js handles Google Pay with PaymentIntents
// Enable in Dashboard → Payment Methods
// Works automatically with the Payment Element
```

### Direct Google Pay API

```typescript
const paymentDataRequest = {
  apiVersion: 2,
  apiVersionMinor: 0,
  allowedPaymentMethods: [{
    type: 'CARD',
    parameters: {
      allowedAuthMethods: ['PAN_ONLY', 'CRYPTOGRAM_3DS'],
      allowedCardNetworks: ['VISA', 'MASTERCARD', 'AMEX'],
    },
    tokenizationSpecification: {
      type: 'PAYMENT_GATEWAY',
      parameters: {
        gateway: 'stripe', // or your processor
        'stripe:version': '2024-12-18.acacia',
        'stripe:publishableKey': 'pk_test_...',
      },
    },
  }],
  merchantInfo: {
    merchantId: 'BCR2DN...', // From Google Pay Console
    merchantName: 'Your Store',
  },
  transactionInfo: {
    totalPriceStatus: 'FINAL',
    totalPrice: '20.00',
    currencyCode: 'USD',
    countryCode: 'US',
  },
};
```

### Common Pitfalls

- `TEST` environment shows all cards, `PRODUCTION` only shows real tokenizable cards
- No direct webhooks — webhooks come from your payment processor
- `merchantId` is required for production (get from Google Pay Console)
- Must comply with Google Pay API Acceptable Use Policy and branding guidelines

---

## 7. Razorpay

**API Model**: REST, Basic Auth (`key_id:key_secret`).
**Base URL**: `https://api.razorpay.com/v1`
**Currency**: INR (amounts in **paise**, not rupees — 1 rupee = 100 paise)

### Core Flow — Orders → Checkout → Verify

```typescript
// Step 1: Create Order (server-side)
const order = await fetch('https://api.razorpay.com/v1/orders', {
  method: 'POST',
  headers: {
    'Authorization': `Basic ${Buffer.from(`${KEY_ID}:${KEY_SECRET}`).toString('base64')}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    amount: 50000, // ₹500.00 in PAISE
    currency: 'INR',
    receipt: orderId,
  }),
});

// Step 2: Checkout (frontend)
const options = {
  key: 'rzp_test_...', // Key ID (not secret!)
  amount: order.amount,
  currency: order.currency,
  order_id: order.id,
  handler: function (response: any) {
    // Send to server for verification:
    // response.razorpay_order_id
    // response.razorpay_payment_id
    // response.razorpay_signature
  },
};
const rzp = new Razorpay(options);
rzp.open();

// Step 3: Verify signature (server-side)
import crypto from 'node:crypto';
const body = razorpay_order_id + '|' + razorpay_payment_id;
const expectedSignature = crypto
  .createHmac('sha256', KEY_SECRET)
  .update(body)
  .digest('hex');

if (expectedSignature === razorpay_signature) {
  // Payment is verified — fulfill order
}
```

### Webhook Verification

```typescript
// Razorpay webhook uses a SEPARATE webhook secret (not your API key_secret)
const webhookSignature = req.headers['x-razorpay-signature'];
const expectedSig = crypto
  .createHmac('sha256', process.env.RAZORPAY_WEBHOOK_SECRET!)
  .update(JSON.stringify(req.body))
  .digest('hex');

if (webhookSignature === expectedSig) {
  // Process webhook event
}
```

### Common Pitfalls

- Amount is in **paise**, not rupees — `50000` = ₹500.00
- Checkout signature uses `key_secret`, webhook uses a SEPARATE `webhook_secret`
- The signature verification string format is `order_id|payment_id` (pipe-separated)
- Must verify payment server-side — never trust client-side callback alone
- Test mode key starts with `rzp_test_`, live with `rzp_live_`

---

## 8. Square

**API Model**: REST, OAuth2 or Access Token.
**Auth**: Bearer token (sandbox or production access token).
**Base URL**: `https://connect.squareupsandbox.com/v2` (sandbox) / `https://connect.squareup.com/v2` (live)

### Core Flow — Payments API

```typescript
const response = await fetch('https://connect.squareupsandbox.com/v2/payments', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${ACCESS_TOKEN}`,
    'Content-Type': 'application/json',
    'Square-Version': '2024-12-18',
  },
  body: JSON.stringify({
    source_id: nonce, // From Square Web Payments SDK
    idempotency_key: crypto.randomUUID(), // REQUIRED
    amount_money: {
      amount: 2000, // $20.00 in cents
      currency: 'USD',
    },
    location_id: process.env.SQUARE_LOCATION_ID!, // REQUIRED
  }),
});
```

### Common Pitfalls

- `idempotency_key` is REQUIRED on all write operations — not optional like some APIs
- `location_id` is required — get from Square Dashboard or Locations API
- Square SDK packages have been deprecated in favor of direct REST API — check latest docs
- Sandbox and production use completely different base URLs
- Webhook signature: HMAC-SHA256 with notification URL as part of the signed content
