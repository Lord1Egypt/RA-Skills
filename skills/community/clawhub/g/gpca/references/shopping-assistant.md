# Shopping Assistant - Detailed Workflows

## Browser Automation

This skill uses OpenClaw's built-in browser. Use these commands:

| Action | Command |
|--------|---------|
| Open URL | `browser open <url>` |
| Read page | `browser snapshot` |
| Click element | `browser click <ref>` |
| Type text | `browser type <ref> "text"` |
| Fill form | `browser fill --fields JSON` |
| Screenshot | `browser screenshot` |
| Wait | `browser wait --text "value"` |

### Browser Profile & Login Persistence

OpenClaw auto-persists cookies and sessions. No user configuration needed. When a user logs into an e-commerce site (e.g., Taobao) in the browser, the session is preserved for subsequent visits.

---

## Auto-Login (Email Verification Code Reading)

GPCA login requires a 6-digit email verification code. Instead of asking the user to check their email manually, read the code automatically via browser.

### Flow
1. Call `gpca_auth_status`. If already authenticated, skip to Shopping Flow
2. Call `gpca_login` with user's email and password — GPCA sends a 6-digit verification code
3. Open the user's email in a browser tab:
   - Detect email provider from the email address domain
   - Navigate to the email provider's web interface
4. Wait for the GPCA verification email to arrive:
   - Take a snapshot to check the inbox
   - Look for an email with subject containing "GPCA" or "verification" or "code"
   - If not found, wait 5 seconds and retry (max 60 seconds total)
5. Open the verification email — click on the GPCA email, take a snapshot to read the body
6. Extract the 6-digit code using pattern matching (`\d{6}`)
7. Call `gpca_verify_login` with the extracted code
8. Confirm login success to the user
9. Navigate the browser back to the shopping task (if applicable)

### Email Provider Detection

| Domain | Provider | URL |
|--------|----------|-----|
| `qq.com` | QQ Mail | `https://mail.qq.com` |
| `gmail.com` | Gmail | `https://mail.google.com` |
| `outlook.com`, `hotmail.com` | Outlook | `https://outlook.live.com` |
| `163.com` | 163 Mail | `https://mail.163.com` |
| `126.com` | 126 Mail | `https://mail.126.com` |

### Email Login State
- **First time**: Guide user to log into their email in the browser manually. The session will persist automatically.
- **Session expired**: If the email inbox requires re-login, inform the user and assist
- **Gmail note**: Google may block automated browser logins. Recommend users use QQ/163/Outlook email for GPCA, or log into Gmail manually first
- **Fallback**: If auto-reading fails after 60 seconds, ask the user to check email manually

### Rules
- NEVER display the verification code in conversation text
- NEVER store email credentials
- Treat the verification code as transient — use it once, then forget
- If auto-reading fails and the user pastes the code in chat, consume it immediately via `gpca_verify_login` — do NOT echo or acknowledge the digits

### Email Privacy & Scope Restrictions
- **Minimum access principle**: Only search for and read GPCA verification emails. Do NOT read, summarize, or process any other emails.
- Snapshot will capture the full inbox page — treat all non-GPCA email content as invisible. Never reference or mention other emails.
- After extracting the verification code, immediately navigate away from the email inbox.
- **First-use disclosure**: Before accessing the email inbox for the first time, inform the user: "I will open your email inbox in the browser to read the GPCA verification code. Your inbox content will be briefly visible to me during this process. Proceed?"
- **Post-login notification**: After auto-login completes, always confirm: "Auto-login completed via email verification code at [timestamp]."

---

## Shopping Flow (7 Steps) - Detailed

### Prerequisites
Before starting a shopping task:
1. Ensure user is authenticated (`gpca_auth_status` or run Auto-Login above)
2. Confirm the user has at least one **activated**, unfrozen card with sufficient balance

### Step 1: Intent Parsing & Funding Check
Parse the user's request to extract:
- **Product**: What to buy (name, specifications, quantity)
- **Budget**: Maximum price willing to pay
- **Site**: Target e-commerce site (default: Amazon)
- **Shipping address**: Ask if not previously provided

Then verify funding:
- `gpca_list_cards` — find activated, unfrozen cards
- **IMPORTANT**: Display card to user only as `**** XXXX` (last 4 digits). Full card number is consumed only in Step 5.
- Check card balances against the estimated budget
- If insufficient: suggest `gpca_deposit_to_card` to fund the card

**Spending Limit Check**:
- Call `gpca_get_spending_limits` to check limits
- Verify estimated budget against `per_transaction`, `daily` remaining, `monthly` remaining
- If any limit exceeded, inform user which limit and remaining allowance. Offer to adjust or cancel.

### Step 2: Product Search
1. Open the target e-commerce site URL in the browser
2. **Domain verification**: Verify current URL domain is in the trusted list. If not, STOP and alert user.
3. Take a snapshot, fill search box, click search
4. Present top 3-5 results (name, price, rating, availability) — ask user to select

### Step 3: Add to Cart
1. Navigate to the selected product page, take a snapshot to confirm details
2. **CONFIRMATION GATE 1**: Present:
   > "Product: [name] — $X.XX
   > Card: **** XXXX (balance: $Y.YY)
   > Proceed to add to cart?"
3. Only after user confirms: Click Add to Cart → Navigate to checkout

### Step 4: Shipping Address
1. If address was provided earlier or from user memory: fill all address fields
2. If no address: ask user for name, street, city, state/province, zip, country, phone
3. Take a screenshot to show the filled address for verification

### Step 5: Payment (SECURITY CRITICAL)
1. **Pre-payment domain check**: Verify current page URL is trusted. If not, STOP.
2. Take a snapshot to identify payment form fields
3. Retrieve card details **at this moment only**:
   - `gpca_list_cards` — card number, expiry date
   - `gpca_get_cvv` — CVV
4. Fill payment form: card number, expiry (MM/YY), CVV, cardholder name
5. **NEVER** repeat card number, CVV, or expiry in conversation

### Step 6: Order Confirmation
1. Take snapshot + screenshot of order summary
2. **CONFIRMATION GATE 2**: Present:
   > "Order total: $X.XX (including $Y.YY shipping, $Z.ZZ tax)
   > Card: **** XXXX
   > [screenshot attached]
   > Confirm purchase?"
3. Only after **explicit** user confirmation: Click Place Order
4. If user cancels: acknowledge and stop

### Step 7: Capture Result
1. Wait for confirmation page, take screenshot + snapshot
2. Extract: order number, estimated delivery date, total charged
3. Present results to user
4. Call `gpca_record_spending` with total and description (e.g., "Amazon - [product name]")

---

## Taobao/Tmall Shopping Flow (China E-Commerce)

Taobao and Tmall do not accept direct credit card input. Payment goes through **Alipay** with a GPCA card bound as the payment method.

### Prerequisites (One-Time Setup)
1. User must have an Alipay account with GPCA card already bound
2. If not bound: guide user to open Alipay → 银行卡管理 → 添加银行卡 → enter GPCA card details
3. **IMPORTANT**: Card binding is done by the user manually — the Agent does NOT handle this step

### Taobao Flow (Replaces Steps 4-5)
Steps 1-3 follow standard flow with differences:
- URL: `https://www.taobao.com` or `https://www.tmall.com`
- Prices in CNY (¥), search results in Chinese

**Step 4: Shipping Address (Chinese format)**
- Fields: 收货人 (name), 手机号码 (phone), 所在地区 (province/city/district), 详细地址 (street address)

**Step 5: Payment via Alipay**
1. Click "提交订单" — redirects to Alipay
2. **Domain verification**: Confirm redirect is to `alipay.com` or `alipayobjects.com`
3. Select bound GPCA card as payment method
4. **GATE 2**: Confirm: "订单金额: ¥X.XX, 支付方式: 支付宝 (GPCA 卡尾号 XXXX), 确认付款?"
5. Alipay may require payment password — escalate to user: "支付宝需要输入支付密码，请在浏览器中完成验证。"

**Security Notes**:
- Agent does NOT enter Alipay payment password
- No card data filled on Taobao/Tmall pages — payment handled by Alipay
- CVV NOT needed at checkout (used during one-time card binding)

### Currency Note
- GPCA card balance in USD, Alipay converts to CNY
- Exchange rate by Alipay/card network, not GPCA
- Warn user about potential FX fees

---

## Session Handling During Checkout
- If any GPCA tool returns `re_login` during checkout:
  1. Pause checkout (do NOT submit with incomplete data)
  2. Run Auto-Login flow to re-authenticate
  3. If during Step 5: re-navigate to payment page and re-fill ALL fields from scratch
  4. For other steps: resume from beginning of current step
- Never leave a half-filled payment form unattended

## Trusted Domains (Whitelist)
Only fill payment information on pages whose domain matches:
- `amazon.com`, `amazon.co.jp`, `amazon.co.uk`, `amazon.de`, `amazon.fr`, `amazon.it`, `amazon.es`, `amazon.ca`, `amazon.com.au`
- `ebay.com`
- `walmart.com`, `target.com`, `bestbuy.com`
- `taobao.com`, `tmall.com` (payment via Alipay)
- `alipay.com`, `alipayobjects.com` (Alipay payment page)
- `jd.com` (京东)

If user requests a site not on this list, confirm: "This site is not in my trusted domain list. Are you sure you want to proceed with payment on [domain]?"

## Escalation
- CAPTCHA: "I've encountered a CAPTCHA. Please complete it in the browser, then tell me to continue."
- 3D Secure: "Your bank requires additional verification. Please complete it in the browser."
- Unexpected errors: Stop, take a screenshot, show the user, and ask how to proceed

## Error Handling

| Error | Action |
|-------|--------|
| Insufficient balance | Suggest funding via `gpca_deposit_to_card` |
| Product out of stock | Inform user, suggest alternatives |
| Email verification timeout (60s) | Ask user to check email manually or resend |
| Browser session lost | Re-navigate and retry |
| Payment declined | Show error, suggest different card |
| Session expired mid-checkout | Run Auto-Login, resume checkout |
| Alipay password required | Escalate to user |
| Taobao login required | Ask user to log in manually |
| GPCA card not bound in Alipay | Guide user to bind card first |
