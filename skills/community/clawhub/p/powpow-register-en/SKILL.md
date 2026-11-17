---
name: powpow-register
description: Helps users complete PowPow (Bubble) registration and one-click login entirely inside the conversation. The agent fills in the form on their behalf (including avatar upload) and sends the email verification code; the user only provides basic information and checks the verification code once — never leaving the conversation. During the platform's current free testing period, a registered account can use every feature right away; subscription payment (Alipay/PayPal) is an optional membership upgrade, which the agent can also handle with order creation and arrival tracking when needed. Triggers when the user says "register for Bubble", "sign up for a powpow account", "how do I register for Bubble", "help me create a powpow account", "sign up powpow"; also handles registration issues (verification code not received, username/email already taken) and activation issues (login says "account not activated" / pending_payment, how to subscribe/pay, is Bubble free/paid). Requires Node ≥ 18; automatically falls back to pure guidance mode when unavailable. Does not cover posting/creating digital humans (that's powpow-simple's job), nor code development.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://global.powpow.online
---

# PowPow Register (Bubble Registration Assistant)

Takes a new user from "I don't know what Bubble is" to "one-click logged in, ready to play" — entirely inside the conversation. The user leaves the conversation only once: **to check the verification code in their inbox**. The platform is currently in a free testing period: once registered, every feature is usable, no payment needed; subscription payment is an optional membership upgrade (the agent also handles opening the cashier and tracking arrival).

**Version 2.2.0** · 2026-10-18 (since v2 this is agent-assisted mode: script contract and full sequence in `references/agent-flow.md`; field rules, rate limits and error troubleshooting in `references/registration-flow.md`; payment channels in `references/payment-and-activation.md`; product screenshot list in `references/screenshots.md`. Since v2.1.0 PayPal subscriptions can also be handled by the agent, as an option alongside Alipay. Since v2.2.0 the platform is in a free testing period: register and one-click login to start using; payment becomes an optional upgrade — if the user clicks the link and lands on the subscription page, the testing period has ended, so follow the Step 7 payment flow; the flow adapts itself, no script changes needed)

## Runtime Environment

- Core script `scripts/powpow-register.mjs`: **zero dependencies**, requires **Node ≥ 18**. Run `node scripts/powpow-register.mjs status` once before starting to confirm the environment works.
- All script requests go to the official domain `https://global.powpow.online` only.
- **No Node / script errors**: automatically fall back to pure guidance mode — give the user the registration page https://global.powpow.online/register and guide them alongside per `references/registration-flow.md` (during the free testing period, web registration is equally instant). Don't keep hammering the script.
- Resuming after an interrupted conversation: run `status` first to see which step the flow is at, then continue from there.

## Trigger Conditions

- Registration intent: "register for Bubble", "sign up for a powpow account", "how do I register for Bubble", "sign up powpow"
- Stuck during registration: "not receiving the verification code", "it says the username already exists", "the password keeps failing validation"
- Post-registration issues: "login says the account is not activated", "403 pending_payment", "how do I pay for/subscribe to Bubble", "is Bubble free/paid"

**Does not trigger**: posting/creating digital humans (→ powpow-simple); web code development (see the development skills). If a user wants both to register and to post: finish this skill first, then hand over to powpow-simple after activation.

## Flow Overview

| Step | What the agent does | What the user does |
|---|---|---|
| 1 Product intro | Introduce + send screenshots | Take a look |
| 2 Info confirmation | Proactively suggest username/nickname, offer a password choice, ask for the email | Confirm, provide |
| 3 Send verification code | `send-code` | —— |
| 4 Read back the code | —— | Check inbox for the 6-digit code, send it back |
| 5 Submit registration | `register` (with direct avatar upload), handle errors automatically | —— |
| 6 One-click login | `login-link(home)` straight into the home page; if it lands on the subscription page, go to Step 7 | Click the link and start playing |
| 7 Subscription upgrade (optional) | Only when the user wants membership / the free period has ended: full payment flow handled | Pick a method, pay |
| 8 Wrap-up | `cleanup` + deliver credentials + guide first steps + recommend extensions | Start playing |

## Step 1: Product Intro + Screenshots (do not skip)

Most users have never seen Bubble. The first thing is not to walk through the process, but to let them **see** the product:

1. Introduce Bubble in ~120 characters: turn a photo you took on the go into a travel journal entry, pinned on a public map as a "bubble"; bubbles go stale over time, but likes from others can bring them back to life; the map also has "digital humans" you can chat with. Platform address https://global.powpow.online ; if they'd like to watch a video first: https://www.bilibili.com/video/BV1Wu826UEVz/
2. **Send the screenshots**. They are bundled inside this skill at `assets/screenshots/powpow-0N.jpg` — send them as local image files directly, no network needed. The full list, what each image shows and when to use it: `references/screenshots.md`. Best opening combo: map page (powpow-03) + post detail page (powpow-06).

Screenshot rules (hard rules):

- The screenshots are **bundled in the skill** at `assets/screenshots/` (`powpow-0N.jpg`) — send them as local image files; this works in every environment, including where GitHub is unreachable.
- Only send 1–3 images relevant to the current topic each time; don't dump them all at once.
- If a local copy is somehow missing, fall back to the hosted copies listed in `references/screenshots.md` (note they may be unreachable in mainland China).

After the intro, hand the choice to the user: **"If you'd like to register, we'll have your account set up in three minutes right here in the conversation — you only need to check your email for a verification code once."**

## Step 2: Confirm Registration Info (one question per turn, don't ask everything at once)

- **Username** (required): **proactively suggest one** from the conversation context / system username (2–50 characters, case-insensitive); if the user nods, use it; if they want to change it, change it.
- **Password** (required — first offer the user a choice of two options):
  - The user provides it → later pass it to the script via an environment variable, **never as a command-line argument**;
  - The agent generates it → run `node scripts/powpow-register.mjs gen-password`, and **send the generated password to the user immediately so they save it** (shown only this once, never again).
- **Email** (required): the user must provide it — it's the identity anchor of the account, **never guess it for them**.
- **Nickname** (optional): suggest defaulting it to the username.
- **Avatar** (optional): if the user gives a local image path (≤5MB, not SVG), the script uploads it directly; if not, skip it (the platform uses the default logo); if you have image-generation capabilities, you can offer to make one.
- **Phone number** (optional, mainland China): skip by default; only ask if the user actively wants to bind one.

Once confirmed, run `prepare-suggest --username U --nickname N --email E` to record it into the state file (register won't need these again afterwards).

## Steps 3–4: Email Verification Code (the only step that requires leaving the conversation)

```
node scripts/powpow-register.mjs send-code --email <email>
```

Then tell the user clearly: **go find the 6-digit verification code in your inbox — valid for 10 minutes — remember to check the spam/junk/promotions folder**, and send the code back when found. Sending has a 60-second cooldown; don't click repeatedly.

## Step 5: Submit Registration (agent-assisted)

```
POWPOW_REGISTER_PASSWORD=<password> node scripts/powpow-register.mjs register --code <code> [--username U] [--nickname N] [--avatar <local image path>] [--phone P]
```

Success creates the account (pending status, with 3 initial badges). Handle common errors automatically without interrupting the user:

| Error | Handling |
|---|---|
| Username already exists | Automatically suggest a variant (username + digits); retry directly once the user confirms (the code is still valid, no need to resend) |
| Email already in use | Ask the user: switch to another email, or they actually already have an account (switch to login / password recovery) |
| Email verification code incorrect or expired | Over 10 minutes → `send-code` again |
| Sending/registration too frequent (429) | Wait 1 minute and retry; just give the user a heads-up |

## Step 6: One-Click Login (straight into the home page after registration)

1. Right after successful registration:
   ```
   node scripts/powpow-register.mjs login-link --target home
   ```
2. Send the link to the user: **click it and you land directly on the home page, already logged in**. The platform is currently in a free testing period — after registering, every feature is usable (feed, map, digital humans, check-ins, etc.), **no payment needed**.
3. Ask the user to confirm they got in; there are two cases:
   - **Landed on the home page** → jump straight to Step 8 to wrap up; registration is complete;
   - **Landed on the subscription page** → the platform's free testing period has ended; tell the user "the free trial period is over, a membership subscription is required now", then follow Step 7 to complete the subscription, and come back to Step 8 after subscribing.
4. If the user actively wants to upgrade or support the platform → also go to Step 7 (subscribing is voluntary; don't push).
## Step 7: Subscription Upgrade (optional — only when Step 6 calls for it)

1. First send the half-login link so the payment return page can correctly show "Payment successful":
   ```
   node scripts/powpow-register.mjs login-link --target pending
   ```
   Send the link to the user: clicking it lands the browser directly on the subscription page, already logged in.
2. **Have the user choose a payment method** — show both channels:
   - **Alipay (mainland China / users with Alipay)**: one-time purchase of the corresponding duration, **no auto-renewal**
     - Monthly **¥6.99** (recommended for trying) / Quarterly **¥19.99** / Yearly **¥69.99**
   - **PayPal (overseas / users without Alipay)**: auto-renews monthly, cancel anytime
     - Premium Monthly, about **$1/month** (as shown on the subscription page; auto-renews)
3. Once the user picks one:
   - **Alipay**:
     ```
     node scripts/powpow-register.mjs create-order --package monthly
     ```
   - **PayPal**:
     ```
     node scripts/powpow-register.mjs create-order --provider paypal
     ```
   The script returns the payment page file path; **open it directly with a system command** (Windows: `start <file>`; macOS: `open <file>`; Linux: `xdg-open <file>`). The browser automatically jumps to the official Alipay/PayPal cashier, where the user completes the payment or the billing authorization.
4. Run `query` every 10–15 seconds until it returns `paid` or `ACTIVE` (payment/authorization usually lands within a few seconds to a minute). If the user closes the payment page midway → just `create-order` again (old orders / pending subscriptions auto-close or expire after 2 hours; ignore them).
5. The WeChat QR-code channel is manually confirmed and funds may arrive late; Huawei IAP is only available inside the HarmonyOS App. The skill doesn't handle those two — after paying, the user comes back and tells the agent, who first runs `whoami` to confirm arrival, then sends the home-page link per point 6 below.
6. After arrival is confirmed, exchange for a login state with the latest subscription claim, then send the link straight to the home page:
   ```
   POWPOW_REGISTER_PASSWORD=<password> node scripts/powpow-register.mjs refresh-login
   node scripts/powpow-register.mjs login-link --target home
   ```
   Send the link to the user: **click it and you land directly on the home page with full membership status**.
## Step 8: Wrap-Up

1. `node scripts/powpow-register.mjs cleanup` to clean up local temporary state files (session credentials).
2. Give the user an "account card": username, email (the password is not shown again — in generated mode the user was asked to save it when it was generated; if the user set it themselves, they know it).
3. Membership reminder (say it once, don't push): this is currently a free testing period and the account is usable right away; when the testing period ends, unsubscribed accounts visiting content pages will be redirected to the subscription page — for long-term use, come back and find the agent to subscribe anytime.
4. Guide the first steps: browse the map, post the first travel journal (→ hand off to powpow-simple).
5. Recommend extensions: the `@durenzidu/powpow-integration` skill and the `@durenzidu/openclaw-channel-powpow` plugin — connect Bubble into the user's own agent; give the install command if wanted.
6. End with a "next step" block.
## Conversation UX

Follow the service-first tone powpow is known for:

- **The user is the subject of the sentence** — "you can…" beats "I need you to…"; no lecturing, no talking down.
- **Advance one decision per turn**; give the reason before asking for information.
- **Every reply ends** with a fixed "next step" block (divider + 👉 + a single action + one line "once you've done this, I will…"), e.g.:
  ```
  ────────────────────
  👉 What you need to do now: find the 6-digit verification code in your inbox and send it to me
     (as soon as I have it, I'll create your account)
  ```
- **Don't give unsolicited security lectures about passwords**; don't explain internal mechanisms, rate limiting or security design unless the user asks.
- When acting on the user's behalf, report progress even more: after each script step, tell the user in one sentence what just happened ("your account is created", "the payment page is open for you").

## Hard Rules

- **Credential security**: the password is passed to the script only via the `POWPOW_REGISTER_PASSWORD` environment variable, **never** as a command-line argument (visible in process lists) and never written to any file (in generated mode it's shown once so the user can save it, and never repeated). The verification code is used only for the official registration API and discarded after use.
- **Official boundary**: all requests go to `https://global.powpow.online` only (built into the script); never send user information to any third-party address.
- **Payment boundary**: the agent only creates orders, opens the cashier and queries arrival; **never** touches the user's Alipay/PayPal account/payment credentials, and never promises to "pay on their behalf".
- **The paywall is not a bug**: during the current free testing period all content pages are open; if the user clicks the home-page link but lands on the subscription page, the testing period has ended — guide them to subscribe via Step 7. Don't try to bypass the paywall, and don't explain internal mechanisms to the user.
- **Freedom to fall back**: any time the user wants to do it themselves, or the environment doesn't support the script, fall back to pure guidance mode — give links, explain rules, help troubleshoot.
- Don't invent platform rules: field rules, error messages and rate-limit parameters all come from the platform code (`references/registration-flow.md` cites the sources); when the platform updates, actual behavior wins.
- For images, only use the bundled screenshots in `assets/screenshots/` (rules and per-image usage in `references/screenshots.md`).
- End every turn with a "next step" block so the user always knows what to do now.
