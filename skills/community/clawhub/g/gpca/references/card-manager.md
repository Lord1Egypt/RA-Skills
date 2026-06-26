# Card Manager - Detailed Workflows

## New User Registration
1. `gpca_get_captcha` — get captcha image (base64 PNG)
2. **Captcha recognition** (with fallback):
   - **If you can see/understand the image**: Read the characters directly and use the code automatically. If uncertain, show the image to the user and ask.
   - **If you cannot process images** (text-only model): The tool also returns `captcha_hint` with a text description. Show the user: "请查看验证码图片并输入上面的字符" and wait for their input.
3. Ask for: email, username, password, confirm password, and optional referral code
4. `gpca_register` with the auto-recognized captcha code — submits registration, sends email verification code.
   - If **captcha error**: retry from step 1 (max 3 attempts).
   - If **"email or username is exists"**: the username may be taken. Auto-retry by appending random digits to the username (e.g., `user123` → `user123_8472`). Get a new captcha first, then call `gpca_register` again. If it still fails, the email is already registered — tell the user to login instead.
5. **Offer auto-login**: "验证码已发送到您的邮箱。我可以帮您自动从邮箱读取验证码（需要在浏览器中打开您的邮箱），或者您也可以手动输入验证码。您选择哪种方式？"
   - If user chooses auto: follow Auto-Login email reading flow in shopping-assistant.md
   - If user chooses manual: ask for the 6-digit code
6. `gpca_finish_register` with `register_id` (from step 4) and verification code
7. Registration complete — proceed to login flow below

## Login (Existing User)
1. Ask for email and password
2. Call `gpca_login` — tells user a verification code was sent to their email
3. **Offer auto-login**: "验证码已发送到您的邮箱。我可以帮您自动从邮箱读取验证码（需要在浏览器中打开您的邮箱），或者您也可以手动输入验证码。您选择哪种方式？"
   - If user chooses auto: follow Auto-Login email reading flow in shopping-assistant.md
   - If user chooses manual: ask for the 6-digit code
   - **Remember user's choice**: If user chose auto-login before, default to auto-login next time without re-asking
4. Call `gpca_verify_login` — completes login

## Forgot Password
1. Ask for the user's registered email
2. `gpca_send_reset_password_email` — sends verification code to email
3. **Offer auto-login**: Same as above — offer to auto-read verification code from email or manual input
4. `gpca_reset_password` with email, verification code, and new password
5. Proceed to login flow

NEVER store or display credentials after use. If any tool returns "Session expired", restart auth.

## Apply for a Bank Card
1. `gpca_check_kyc` — verify KYC is approved. If not, guide user through KYC first
2. `gpca_supported_cards` — show available card types (Mastercard/Visa, virtual/physical)
3. Ask user which card type they want
4. `gpca_order_virtual_card` with selected card_type_id
5. Confirm success and next steps (activation)

## Recharge USDT (Receive crypto to wallet)
1. `gpca_supported_chains` — list available blockchain networks
2. Ask user which chain to use (or pick default)
3. `gpca_deposit_address` with chain_id — get wallet address
4. Display the address clearly. Tell user to send USDT to this address on the selected chain
5. Warn: only send USDT on the correct chain, wrong chain = lost funds

## Transfer USDT to Bank Card (USDT → USD)
1. `gpca_wallet_balance` — show current USDT balance
2. `gpca_bank_card_list` — list eligible cards
3. Ask user: which card and how much to transfer
4. **CONFIRM** the operation: "Transfer X USDT (≈ $X USD) to card ending in XXXX?"
5. Only after user confirms: `gpca_deposit_to_card` with card_id and amount
6. Show result

## Check Balances
- USDT wallet: `gpca_wallet_balance`
- All cards: `gpca_list_cards` — show each card's balance
- Display amounts with 2 decimal places and currency symbol

## View Transaction History
- Card transactions: `gpca_card_transactions` with card_id and optional date range
- Wallet transactions: `gpca_wallet_transactions` with optional date range
- Default to last 7 days if no range specified

## Card Management
- Activate: `gpca_activate_card`
- Freeze/unfreeze: `gpca_freeze_card`
- Change PIN: `gpca_change_pin` (needs old + new PIN)
- Reset PIN: `gpca_reset_pin`
- Get CVV: `gpca_get_cvv` — warn about security before revealing

## KYC Verification
1. `gpca_check_kyc` — check current status
2. If needed: `gpca_request_kyc` (Mastercard) or `gpca_request_kyc_visa` (Visa)
3. Upload documents: `gpca_add_kyc_file` with base64 data
4. Submit: `gpca_submit_kyc`

## Spending Limits (Agent-side soft limits)
Set per-transaction, daily, and monthly spending limits for shopping. Limits are enforced locally by the MCP server.

- **Set limits**: `gpca_set_spending_limit` — set `per_transaction`, `daily`, and/or `monthly` limits (USD). Merges with existing limits.
- **View limits**: `gpca_get_spending_limits` — returns current limits, today's/month's spending totals, and remaining allowances.
- **View records**: `gpca_spending_summary` — get spending records for `"today"`, `"month"`, or `"all"`.
- **Remove limits**: `gpca_remove_spending_limit` — remove a specific limit type or `"all"`.
- **Record spending**: `gpca_record_spending` — called automatically after a successful shopping purchase (Step 7).

Spending limits are checked before Shopping Gate 1. Data is stored locally in `data/limits.json` and `data/spending.json`.
