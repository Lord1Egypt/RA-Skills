---
name: "google-autoreply"
description: "Onboard a merchant into the Auto Google Review Reply product: register/login, connect a Google Business Profile, benefit from a 5-day free trial (membership check, no forced payment), and configure AI auto-reply. Invoke when the user wants to set up an account, connect Google Business, check membership/ trial status, or enable AI review auto-reply."
---

# Auto Google Review Reply - Merchant Onboarding

This skill drives an AI agent to onboard a merchant end-to-end into the **Auto Google Review Reply** product. It guides the AI to (1) get the merchant signed in, (2) connect a Google Business Profile, (3) confirm membership / free-trial status (new shops get a 5-day free trial and are **not** forced to pay), and (4) configure the AI review auto-reply. The AI talks to the merchant and calls the real backend REST APIs.

## Product Context

- **Login account and Google Business account do NOT need to be the same.** The merchant signs in to the product with any product account (username/password or a Google sign-in with any account), then separately authorizes Google Business with the Google account that manages the Business Profile. They can be different accounts.
- Backend responses use the envelope `{ code: 200, message, data }`. Treat `code !== 200` as an error and surface `message` to the merchant.
- **Token storage (designated location = environment variables).** All secrets are kept out of the prompt, URL and logs, and stored in a single designated place: environment variables. Do not hard-code tokens in code/URLs, and never send them as query params. Designated variables:
  - `AUTH_TOKEN` — the full `Authorization` header value for the login/session token (e.g. `Bearer <token>`). Set once after Step 1 and reused verbatim for **every** backend API call and the next session. Re-authorize only when the API returns `401`.
  - GMB OAuth client credentials (`client_id`/`client_secret`) are read by the backend from Spring config (`spring.security.oauth2...client-id/secret`), **not** by the agent — no env var needed.
  - Google Business `access_token`/`refresh_token` are **owned and persisted by the backend** in the shop's `googleBusinessToken` (DB) and auto-refreshed; the agent never stores or forwards these. A once-made GMB connection stays valid.
  - **Token lifetime (checked)**: login/session JWT is long-lived (`jwt.expiration` ≈ 7 years). GMB `access_token` is short-lived (`expires_in`, typically ~3600s / 1h), `refresh_token` is long-lived — the backend refreshes automatically.
  - To read a stored value for diagnostics, print only a masked/truncated version (e.g. first 6 chars), never the full token.
- If the agent has NO browser automation (no `browser-skill` / `opencli-browser`), do NOT ask the merchant to copy/paste the token. Use the **SSO handoff** mechanism described in Step 1 — the agent gets the token by polling a backend endpoint, so the merchant only has to complete the sign-in.
- **Membership / free trial**: the 5-day free trial is **granted automatically when the merchant creates their first shop** — `POST /shop/create` sets the shop's `vipExpireTime = now + 5 days` (and `vipLevel = basic`) on first shop creation. No extra runtime check is needed; the existing VIP logic treats the trial as a valid membership. During the trial (i.e. while `vipExpireTime` is in the future) auto-reply works without payment. Once `vipExpireTime` passes and there is no renewed membership, the merchant must subscribe (Stripe) before auto-reply works. Membership status is read from the existing endpoint `GET /shop/getCurShop` (`vip_expire_time` / `vipLevel`); never force payment for a shop whose trial is still active.

### Backend base URL & OAuth endpoints (from `utils/appConfig.js`)

```
API_BASE_URL  = https://apprest.mytruststores.com/adminServer
OAuth login   = {API_BASE_URL}/oauth2/authorization/google-autoreply
Connect Google Business = {API_BASE_URL}/oauth2/connectGoogleBusiness?token=<url-encoded-token>&redirectState=<url-encoded-return-url>
```


## Before You Start - Gather From The Merchant

Ask the merchant (use a checklist/AskUserQuestion style) for:

1. Does the merchant already have an account in this product? (yes / no)
2. Which Google account manages (owns or has manager access to) the Google Business Profile they want to use? They authorize with this account during the Google Business connect step — it does NOT have to match the login account.
3. What is the business / store (the Google Business Profile location) they manage?
4. Auto-reply preferences: trigger star threshold (1–5), reply language (auto follow customer / zh / en / fr / es / it), shop intro, signature, keywords.

> Note: No payment is required up-front. New shops have a 5-day free trial. Do not ask which subscription plan they want until/unless the membership check shows the trial has ended and they are `EXPIRED`.

## Workflow

The onboarding is strictly sequential. Do not skip ahead. After each step, confirm success before moving on.

### Step 1 - Log In / Register

The sign-in account does NOT need to be the Google Business owner. Any product account works.

> **Browser security prompt ("encrypt access / direct access")**: workbuddy or the browser may warn because the URL carries a token or uses plain HTTP (`http://`). To avoid it:
> - Prefer the **SSO handoff (Mode B)** below so the URL only contains `handoffId` — the token never appears in the address bar, so no sensitive-URL warning.
> - If you must open a URL in the browser, always pick **"encrypt access" (HTTPS)** — the production base URL `https://apprest.mytruststores.com` is already encrypted, so this is safe. Do NOT pick "direct access" on plain HTTP.

**Recommended path: Google OAuth sign-in (no account-identity constraint).**

1. Build the login URL: `{API_BASE_URL}/oauth2/authorization/google-autoreply`.
2. Tell the merchant to sign in with any Google account (there is no requirement that it matches the Business Profile).
3. The callback carries `?token=<token>`; store `Bearer <token>` as the session token (in web: `localStorage`; in app: uni storage under key `token`).
4. Verify the session is valid:
   - `GET /admin/info` (header `Authorization: Bearer <token>`) -> expect `code === 200` and a user object.

**Getting the token automatically — two modes, pick by ability:**

- **Mode A (agent has browser automation):** open the login URL, read `token` from the callback URL, store `Bearer <token>`.
- **Mode B (agent has NO browser automation):** use the **SSO handoff** so the merchant never copy/pastes:
  1. `POST /oauth2/handoff/create` with `returnUrl=<the calling app's return URL>` (e.g. a URL the invoking application — workbuddy / openclaw — listens on). Response `data.handoffId` (one-time slot, usable for 3 min). If `returnUrl` is omitted the login falls back to the product login page.
  2. Give the merchant this URL: `{API_BASE_URL}/oauth2/authorization/google-autoreply?handoffId=<handoffId>` and ask them to complete the sign-in. After login the browser is **redirected back to `returnUrl` with `token` & `tokenHead` appended** (e.g. `returnUrl?token=...&tokenHead=...`).
  3. Poll `GET /oauth2/handoff/<handoffId>/token` (every ~2–3s) until `data.status === "READY"`.
     - `PENDING` → keep polling.
     - `EXPIRED` → the slot expired / was never opened; create a new handoff and retry, or fall back to asking the merchant to paste the `?token=` value.
  4. On `READY`, take `data.authorization` (e.g. `Bearer <token>`, exactly the `Authorization` header value). It is single-use — the slot is deleted after being read.

**Fallback: username/password register.**

- Register: `POST /sso/register` with `{ username, password, telephone, authCode }`. If a SMS code is needed, send it via `POST /admin/sendSmsCode`.
- Login after register: `POST /sso/login` (URL-encoded form) with `{ username, password }` -> returns `data.tokenHead + data.token`, store as `Bearer <token>`.
- Or login directly via `POST /admin/login` with `{ username, password }`.

If the merchant already has an account, skip register and just log in.

*Success check*: `GET /admin/info` returns `code === 200`. Otherwise, stop and help the merchant retry.

### Step 2 - Connect Google Business Profile

The merchant authorizes Google Business with the account that manages the Business Profile (may differ from the login account).

1. Check current connection status: `GET /google-business/status`. This only reports connection/token metadata (`connected`, `tokenValid`, `createdAt`, `expiresIn`) — it does **NOT** return `shopName`/`businessName`. To read the currently bound merchant, use `/locations/current` (see below).
2. If not connected, initiate OAuth connect. Build:
   ```
   {API_BASE_URL}/oauth2/connectGoogleBusiness?token=<url-encoded-token>&redirectState=<url-encoded-return-url>
   ```
   In H5, the return URL is the current page; in the app it is `yingrestSeller://pages/user/seo/connect`.
3. The merchant authorizes with the Google account that manages the Business Profile. After the callback (H5: URL contains `succ=true`), re-check `GET /google-business/status` until it shows connected.
4. Fetch the selectable locations and the currently bound merchant in one call: `GET /google-my-business/locations/current`.
   - Response shape: `{ list: [...], current: {...}, selectable: boolean }`.
   - `current` is the **currently bound merchant** (its `locationId`, `title`/name, etc.); `list` is every selectable location for the account. Confirm the correct location with the merchant, defaulting to `current`.
   - **Empty state**: when the account has no Google Business stores, `list` is `[]` and `current` is `null`. In that case report "此账户下没有谷歌店铺信息" to the merchant, and do not proceed to bind a location.
5. Bind the chosen location: `POST /google-my-business/locations/bind` with `{ locationId }` (or the location name / raw id prefixed `locations/...` — normalize by stripping the `locations/` prefix).
   - Helpful read-only helper: `GET /google-my-business/business-locations/{accountId}`.

*Success check*: `GET /google-my-business/locations/current` shows `data.current` with the expected merchant. If the merchant picked the wrong profile, unbind with `POST /google-business/disconnect` and redo.

### Step 3 - Check Membership / Free Trial (no forced payment)

The 5-day free trial is granted automatically at registration and written into `vipExpireTime`. Only require payment when the trial has ended and the merchant is not a valid member.

1. Check membership via the existing endpoint: `GET /shop/getCurShop` (response `data` includes `vip_expire_time` and `vipLevel`). Determine validity from `vip_expire_time`:
   - `vip_expire_time` in the future → **ACTIVE** (covers the auto-granted 5-day trial and paid plans).
   - `vip_expire_time` null or in the past → **EXPIRED**.

2. Decide:
   - **ACTIVE** → the merchant has a valid trial/membership; proceed to Step 4.
   - **EXPIRED** → the free trial ended and there is no active membership. Inform the merchant the trial is over and ask them to subscribe before auto-reply will work:
     - Confirm the plan with the merchant: `monthly` (`Review_Basic_Monthly`, amount 10) or `yearly` (`Review_Basic`, amount 100).
     - Create a checkout session: `POST /pay/stripe/checkout` with `{ productId, amount }`. Response `data.checkoutUrl` is the Stripe hosted checkout URL.
     - Send the merchant to `checkoutUrl` to pay. Optionally verify with `GET /pay/history` (or `GET /pay/config`).
3. After any payment, re-check `GET /shop/getCurShop` → `vip_expire_time` should now be in the future.

*Success check*: membership is valid (`vip_expire_time` in the future). Never proceed past this step while expired for auto-reply (the backend returns `403001`/`403002` when the VIP is expired).

### Step 4 - Configure AI Auto-Reply

Auto-reply config lives under the news/auto-review APIs, per store.

1. Load current config: `GET /news/getAutoReviewsList`. If empty, we will create; otherwise we update the existing entry.
2. (Recommended) Let the AI auto-generate a full config from the Business Profile: `POST /ai/generateCustomerConfig` with `{ businessId, language }`, after confirming remaining quota via `GET /ai/generateCustomerConfig/status`.
   - AICustomer config includes `sign`, `shopIntroduction`, `advancedTips`, `keywords`, `maxLength`.
3. Configure the reply rules. The payload shape:
   ```json
   {
     "sign": "<signature, optional>",
     "translaSign": true,
     "advancedTips": "<extra AI instructions, optional>",
     "shopIntroduction": "<shop intro, optional>",
     "startCount": 1,
     "status": 1,
     "maxLength": 100,
     "replyLanguage": "auto",
     "keywords": ["<keyword1>", "<keyword2>"],
     "aiReplyType": 1
   }
   ```
   - `startCount` = minimum star rating to auto-reply (1–5).
   - `status` = `1` to enable, `0` to disable.
   - `replyLanguage` = `auto` (follow the customer's language) or a fixed locale (`zh`/`en`/`fr`/`es`/`it`).
4. Save:
   - Create: `POST /news/autoReviews` with the payload.
   - Update: `POST /news/updateAutoReviews` with `{ id: <existingId>, ...payload }`.
5. Add merchant keywords to the store so they can be toggled in auto-reply:
   - List store keywords: `GET /news/{shopId}/keywords` (shopId = selected store id).
   - Add: `POST /news/{shopId}/keywords/add` with `{ keyword }`.
   - Delete: `POST /news/{shopId}/keywords/{keywordId}/delete`.
6. Optionally preview a reply for a sample review: `POST /google-my-business/reviews/ai-reply` with `{ commentText, starRating, keywords, sign, maxLength, shopIntroduction, advancedTips, aiReplyType: 1 }`.

*Success check*: `GET /news/getAutoReviewsList` returns an entry with `status` enabled and the chosen rules, and the store keywords list is populated.

## API Reference Summary

| Purpose | Method | Path |
|---|---|---|
| Create SSO handoff slot | POST | `/oauth2/handoff/create` |
| Poll SSO handoff token | GET | `/oauth2/handoff/{handoffId}/token` |
| Register | POST | `/sso/register` |
| Login (username/password) | POST | `/sso/login` |
| Login (account) | POST | `/admin/login` |
| Send SMS code | POST | `/admin/sendSmsCode` |
| Current user info | GET | `/admin/info` |
| Current shop info & membership (trial included via `vip_expire_time`) | GET | `/shop/getCurShop` |
| Connection status (token meta only, **no shopName**) | GET | `/google-business/status` |
| Disconnect Google Biz | POST | `/google-business/disconnect` |
| Current bound merchant + selectable locations | GET | `/google-my-business/locations/current` |
| Bind location | POST | `/google-my-business/locations/bind` |
| Account locations helper | GET | `/google-my-business/business-locations/{accountId}` |
| Auto-reply config list | GET | `/news/getAutoReviewsList` |
| Create auto-reply config | POST | `/news/autoReviews` |
| Update auto-reply config | POST | `/news/updateAutoReviews` |
| List store keywords | GET | `/news/{shopId}/keywords` |
| Add keyword | POST | `/news/{shopId}/keywords/add` |
| Delete keyword | POST | `/news/{shopId}/keywords/{keywordId}/delete` |
| AI auto-generate config | POST | `/ai/generateCustomerConfig` |
| AI config remaining quota | GET | `/ai/generateCustomerConfig/status` |
| AI reply preview | POST | `/google-my-business/reviews/ai-reply` |
| Stripe checkout (only after trial ends) | POST | `/pay/stripe/checkout` |
| Pay history | GET | `/pay/history` |
| Pay config | GET | `/pay/config` |

## Key Constraints & Troubleshooting

- **Account independence**: login account and Google Business account are unrelated. The merchant can sign in with any product account and authorize Google Business with whichever account manages the Business Profile. If the wrong profile was connected, use `POST /google-business/disconnect`, then connect again.
- **No shopName in `/google-business/status`**: that endpoint only reports connection/token metadata. To read the currently bound merchant, always use `GET /google-my-business/locations/current` and inspect `data.current`.
- **Free trial**: the 5-day free trial is granted automatically at registration and written into `vipExpireTime`. `GET /shop/getCurShop` returns `vip_expire_time` — while it is in the future, do not collect payment; only when it has passed do you guide the merchant to a Stripe checkout.
- **Token presence**: All calls require `Authorization: Bearer <token>` — reuse the persisted `AUTH_TOKEN` env var for every request. If `401` is returned, the session token expired/absent — re-run Step 1. (Google Business `access_token` is ~1h but the backend auto-refreshes it with the long-lived `refresh_token`; no manual re-authorization is needed for the connection.)
- **Membership gate**: Backend codes `403001` / `403002` mean the merchant has no valid VIP **and** the free trial has ended — they must subscribe (Step 3) before auto-reply works. During the free trial these codes are not returned.
- **Envelope errors**: Any `code !== 200` is an error; display `message` to the merchant, do not silently proceed.

- **Do not create a Business Profile for the merchant.** Only select an existing authorized location.
