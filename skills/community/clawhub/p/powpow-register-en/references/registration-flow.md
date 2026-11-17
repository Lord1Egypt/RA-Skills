# Registration Flow in Detail — powpow-register

Reference for troubleshooting. All rules come from the platform source code (consistent Next.js frontend/backend validation), with sources cited.
When the platform updates, the live behavior is authoritative.

## Entry Points

- Registration page: https://global.powpow.online/register
- Login page: https://global.powpow.online/login
- Subscription page: https://global.powpow.online/subscription
- If the user arrives via a shared link carrying `?next=...`, they will be automatically returned to the original page after registration + payment.

## Form Fields and Rules

| Field | Required | Rule | Source |
|---|---|---|---|
| Avatar | Optional | Image ≤5MB, SVG not supported; server compresses automatically (>100KB compressed to 400×400 / quality 90) | `src/app/api/auth/register/route.ts` |
| Username | Required | 2–50 characters, trimmed and stored in **lowercase** (Tom and tom are treated as the same username; both registration and login are case-insensitive) | same as above (zod schema) |
| Password | Required | 8–100 characters, must contain uppercase letters, lowercase letters and digits | same as above |
| Confirm password | Required | Must match the password (frontend-only validation) | `src/app/(public)/register/page.tsx` |
| Nickname | Optional | ≤100 characters; defaults to the username if left blank | register route |
| Email | **Required** | Valid email format, ≤255 characters; one email can only register one account | register route |
| Email verification code | **Required** | 6 digits; **valid for 10 minutes**; burned once verified; resending marks the old code as used | `src/lib/email-verification.ts` |
| Phone number | Optional | Mainland-China phone number starting with `1[3-9]`, 11 digits total; one phone number can only be bound to one account | register route |

The page also offers three third-party login buttons: **Google, Watcha, Huawei account** (`GoogleSignInButton` / `WatchaLoginButton` / `HuaweiLoginButton`). Third-party accounts have no local password; trying to log in with a password later returns "该账号未设置密码，请使用其他方式登录" (This account has no password set, please use another login method).

## Rate Limits and Anti-Brute-Force Parameters

| Behavior | Limit | Source |
|---|---|---|
| Registration submit | **3 times/min/IP**, 429 when exceeded | `src/lib/rate-limit.ts` `REGISTER_RATE_LIMIT` |
| Send verification code | Same IP 1/min **and** same email 1/min, 429 when exceeded; frontend button has a 60-second countdown | `src/app/api/auth/register/send-code/route.ts` |
| Code verification | Max **5 attempts** per email within 10 minutes; once the cap is reached the code is rejected even if correct — a new code must be requested | `src/lib/email-verification.ts` |
| Forgot-password code | 1/min/IP | `src/app/api/auth/forgot-password/route.ts` |
| Login | 5/min/IP; **5 consecutive failures lock the account for 30 minutes** (423), with a decreasing remaining-attempts hint during the window | `src/app/api/auth/login/route.ts`, `rate-limit.ts` |

**Privacy protection behavior**: when sending a verification code / forgot-password code, the API returns the same success message whether the email is registered or not, so it never leaks whether an email exists.

## Equivalence of Agent-Assisted Mode and Web Registration

The skill script calls **the same set of public APIs** (`/api/auth/register`, `send-code`, `login`,
`/api/auth/me`) as the registration page form — identical validation, rate limits and error paths — so every rule in
this file applies equally to both modes. Script sequence and command contract: `references/agent-flow.md`.

## Status Flow After Successful Registration

> **Free testing period (starting 2026-10-18; actual platform behavior prevails)**: a newly registered account can **use every feature directly**
> (feed, map, digital humans, check-ins, etc.) with no payment required; unsubscribed accounts are no longer walled off from content pages. The "pending interception"
> described in this section is the regular state after the testing period ends — when that time comes, actual online behavior prevails.

1. The user is stored with `accountStatus: 'pending'` and **3 initial badges** (register route).
2. The server also plants two HttpOnly cookies: the JWT (can access pages directly) and the pendingUserToken (identity credential for the subscription flow).
3. In the regular state (testing period over / no free period), the registration page detects `pending_payment` → redirects to `/subscription`
   (keeping the `next` return parameter); in agent-assisted mode, `me?token=…&redirect=/subscription` achieves the same effect.
   **During the free testing period this step doesn't trigger** — after registering, go straight to the home page and start using.
4. Payment complete → `accountStatus` becomes `active` (**Alipay activates automatically server-side via notify**;
   PayPal activates via Webhook; WeChat QR code is manually confirmed; Huawei IAP goes through `activate-huawei`).
   See `payment-and-activation.md` for details.

In the regular state, inactive (pending) users calling core APIs (feed, map, digital-human chat, check-ins, etc.) get 403;
shared post links are the exception (kept publicly accessible). During the free testing period this interception is suspended and everything is open.
## Common Error Lookup Table

| Message | Cause | What to do |
|---|---|---|
| 「用户名已存在」(Username already exists) | Username is taken (case-insensitive) | Choose a different username |
| 「邮箱已被使用」(Email already in use) | Email is already registered | Use a different email; or log in and use "Forgot password" to recover the old account |
| 「邮箱验证码错误或已过期」(Email verification code is incorrect or expired) | Code mistyped / over 10 minutes / rejected after more than 5 attempts | Click "Resend" and use the code from the **latest** email |
| Verification code not received | 60-second rate limit; or it landed in spam/junk | Wait for the countdown to finish before resending; check the spam folder |
| 「手机号已被使用」(Phone number already in use) | Phone number is bound to another account | Remove the phone number (optional field) or use a different one |
| 「注册请求过于频繁」/ 429 (Registration requests too frequent) | Hit the 3 registrations/min/IP cap | Wait a few minutes and try again |
| 409「用户名或邮箱已被注册」(Username or email already registered) | Collided with another user at submit time (concurrency fallback) | Change the username or email and retry |
| 「图片大小不能超过5MB」/「不支持 SVG」(Image size cannot exceed 5MB / SVG not supported) | Avatar doesn't comply | Use a different image or skip the avatar |
| User clicks the login link but lands on the subscription page (instead of the home page) | The free testing period has ended and the platform paywall is back | Follow Step 7 in SKILL.md for the subscription payment flow; after subscribing, run `refresh-login` and then send the home-page link |
| Registered successfully but login returns 403 "请完成订阅以激活账户" | The account is still pending, and the platform is not in a free testing period (the expected state before payment) | Won't happen during the free testing period; if it does, the testing period has ended — complete the subscription first; if still 403 after payment, an old JWT was used — in script mode run `refresh-login` first to exchange for a new login state |
| Login 423「账户已锁定」(Account locked) | Password entered incorrectly 5 times | Wait 30 minutes |
| Login 401「还剩 N 次尝试机会」(N attempts remaining) | Wrong password, close to being locked | Think carefully before trying again, or go straight to "Forgot password" |
| 「该账号未设置密码，请使用其他方式登录」(This account has no password set, please use another login method) | Third-party (Google/Watcha/Huawei) account | Log in with the original third-party button |
| 「该账号已注销」(This account has been deactivated) | Account is deactivated | A new registration is required |

## Login Tips (handy for troubleshooting too)

Login accepts one combined field of **username / email / phone number** (any of the three works as the account name).
Forgot password: login page → "Forgot password" → enter the registered email, receive a 6-digit code → reset.
