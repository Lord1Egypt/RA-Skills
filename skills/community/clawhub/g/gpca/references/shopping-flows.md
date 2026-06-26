# Shopping Flows & Site-Specific Tips

## Amazon (Primary Target)

### Search
- URL: `https://www.amazon.com` (or regional: `.co.jp`, `.co.uk`, `.de`)
- Search box: typically `#twotabsearchtextbox` or `input[name="field-keywords"]`
- Search button: `#nav-search-submit-button`

### Checkout Flow
1. "Add to Cart" button → cart page
2. "Proceed to checkout" → address page
3. Address form fields: full name, street (line 1 + line 2), city, state, zip, country, phone
4. "Use this address" → payment page
5. Payment: card number, name on card, expiry (MM/YY), CVV in separate fields
6. "Place your order" → confirmation page

### Common Issues
- **Prime upsell popups**: Look for "No thanks" or "Skip" buttons to dismiss
- **Multiple delivery options**: Select standard shipping unless user specifies otherwise
- **Gift option prompts**: Decline unless user requests
- **Address suggestion popups**: Accept the suggested address if it matches, or keep original

---

## eBay

### Search
- URL: `https://www.ebay.com`
- Search box: `#gh-ac-box`
- May show "Buy It Now" vs "Auction" — prefer "Buy It Now" for instant purchase

### Checkout
- "Buy It Now" → checkout
- May require PayPal or direct card payment — select "Add a new card"
- Address and payment fields are standard

---

## Taobao / Tmall (淘宝 / 天猫)

### Search
- URL: `https://www.taobao.com` (淘宝) or `https://www.tmall.com` (天猫)
- Search box: `#q` or `input[name="q"]`
- Search button: `.btn-search` or button near search box
- Results page: product cards with title, price (¥), shop name, sales count

### Login
- Taobao requires login before checkout (淘宝账号)
- Login methods: password, SMS code, or Alipay scan
- If not logged in: take a snapshot to detect login prompt, escalate to user
- **Agent does NOT handle Taobao/Alipay login** — user must log in manually first

### Checkout Flow
1. Product page → "立即购买" (Buy Now) or "加入购物车" (Add to Cart)
2. Cart page (`https://cart.taobao.com`) → select items → "结算" (Checkout)
3. Address page: 收货人, 手机号码, 所在地区 (province/city/district dropdown), 详细地址
4. "提交订单" (Submit Order) → redirects to Alipay
5. Alipay payment: select bank card → enter payment password (user does this)
6. Payment result → order confirmation

### Common Issues
- **Login wall**: Taobao requires login to view some prices and all checkout pages. Ensure user is logged in first.
- **Coupons/红包**: Taobao may auto-apply coupons. Note the discount in Gate 2 confirmation.
- **店铺优惠 (Shop discounts)**: May require minimum purchase amount — inform user if applicable.
- **运费 (Shipping fee)**: Some items have separate shipping fees, shown at checkout. Include in final price confirmation.
- **Cross-border items (全球购/海外直购)**: May have longer shipping times and customs fees. Alert user.

### JD.com (京东)
- URL: `https://www.jd.com`
- Search: `#key` input
- Checkout: "去结算" → address → payment (supports bound bank card or 京东支付)
- JD supports direct bank card payment without Alipay in some cases

---

## General E-Commerce Tips

### Form Field Detection Strategy
The AI agent should use page snapshots to identify form fields by:
1. **Accessibility labels** (preferred): `aria-label`, `label[for]`, snapshot ref IDs
2. **Placeholder text**: `placeholder="Card number"`
3. **Input names**: `name="cardNumber"`, `name="cvv"`
4. **Nearby text**: Look for text labels adjacent to input fields

### Address Reuse
- Store the user's shipping address in conversation memory after first use
- On subsequent purchases, offer to reuse: "Use the same address as last time? (Name, Street, City...)"
- Always confirm before auto-filling

### Price Verification
- Capture the price at Step 3 (add to cart)
- Verify the total at Step 6 (before placing order)
- If the final total exceeds the original price by more than 20% (due to tax/shipping), alert the user

### Multi-Item Orders
- For multiple items, repeat Steps 2-3 for each item before proceeding to checkout
- Show a running total to the user
- **Gate 1** fires once after all items are in cart: confirm the combined cart total + card selection
- **Gate 2** fires at final checkout as normal: confirm final total with screenshot
- Both gates are mandatory per SHOPPING-SKILL.md safety rules

---

## Email Provider Tips

### QQ Mail (`mail.qq.com`)
- Login may require QQ number + password, or QQ scan code
- Inbox: look for email list items, newest first
- GPCA emails typically have subject containing "验证码" or "verification code"
- The 6-digit code is usually in the email body, often in a highlighted or bold format

### Gmail (`mail.google.com`)
- Google may block automated browser logins — recommend users log in manually in the browser profile first
- Inbox: emails listed with sender and subject
- Use the search bar to search "GPCA" if inbox is crowded
- Promotions tab: GPCA emails may land in Promotions — check there if not in Primary

### Outlook (`outlook.live.com`)
- Login with Microsoft account
- Focused/Other inbox: GPCA emails may be in "Other" tab
- Search: use the search bar at top

### 163 / 126 Mail
- Similar to QQ Mail
- Login with email + password
- Look for "验证码" in subject line

---

## Timeout & Retry Strategy

| Operation | Timeout | Retry Strategy |
|-----------|---------|---------------|
| Email verification code arrival | 60s | Check every 5s, then ask user to resend |
| Page load | 15s | Retry navigation once, then report error |
| Add to cart | 10s | Retry click once |
| Payment form submission | 30s | Do NOT retry — risk of double charge |
| Order confirmation page | 30s | Wait, then take screenshot of whatever loaded |
