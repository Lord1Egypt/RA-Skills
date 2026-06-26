# Common User Flows

## First-Time User (No Account)
1. `gpca_auth_status` → not authenticated
2. Ask: "Do you have a GPCA account?" → No
3. `gpca_get_captcha` → display captcha image to user
4. Collect: email, username, password, confirm password, captcha code
5. `gpca_register` → returns `register_id`, sends email verification code
6. `gpca_finish_register` with register_id + verification code → account created
7. Proceed to Login flow below

## Login (Existing User)
1. `gpca_auth_status` → not authenticated
2. Collect email and password
3. `gpca_login` → sends 6-digit email verification code
4. **Offer auto-login**: "我可以帮您自动从邮箱读取验证码，或者您手动输入。选择哪种？"
   - Auto: 在浏览器中打开邮箱 → 找到 GPCA 邮件 → 提取验证码（详见 shopping-assistant.md）
   - Manual: 用户手动输入验证码
5. `gpca_verify_login` → authenticated

## Forgot Password
1. Collect user's registered email
2. `gpca_send_reset_password_email` → sends verification code
3. Collect verification code + new password
4. `gpca_reset_password` → password reset
5. Proceed to Login flow

## New User Journey (After Registration + Login)
1. Complete KYC → `gpca_check_kyc` → `gpca_request_kyc` → upload docs → `gpca_submit_kyc`
2. Wait for KYC approval
3. Apply for card → `gpca_supported_cards` → `gpca_order_virtual_card`
4. Activate card → `gpca_activate_card`
5. Deposit USDT → `gpca_supported_chains` → `gpca_deposit_address` → user sends USDT
6. Transfer to card → `gpca_deposit_to_card` (USDT → USD)
7. Use card for purchases (Amazon, etc.) — see shopping-assistant.md

## Quick Balance Check
1. `gpca_auth_status` → verify logged in
2. `gpca_wallet_balance` → USDT balance
3. `gpca_list_cards` → all card balances

## Fund Card for Purchase
User says: "I want to add $100 to my card for shopping"
1. `gpca_wallet_balance` → check USDT available
2. `gpca_bank_card_list` → pick target card
3. Confirm amount and card with user
4. `gpca_deposit_to_card` → execute transfer

## Troubleshooting
- "Card not working" → `gpca_list_cards` check card status, may need activation
- "Can't apply for card" → `gpca_check_kyc` verify KYC status
- "Where to send USDT" → `gpca_supported_chains` + `gpca_deposit_address`
