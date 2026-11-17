# powpow-register

The PowPow Bubble registration assistant (OpenClaw edition): takes a new user from "I don't know what Bubble is" to
"account activated, one-click logged in, ready to play" — product intro (with UI screenshots), agent-assisted registration
(including avatar upload), Alipay/PayPal subscription order creation with arrival tracking, dual-link one-click login, and error troubleshooting.

**Since v2.0.0 this is agent-assisted mode, and since v2.2.0 it adapts to the platform's free testing period**: the core script `scripts/powpow-register.mjs` is zero-dependency
(Node ≥ 18); the user leaves the conversation only once: to check the verification code in their inbox. During the current free testing period, a registered account can use every feature right away — subscription payment is an optional upgrade; if the testing period ends and the user lands on the subscription page, the flow switches to the payment path automatically. Without Node, or when the user prefers to do it themselves, it automatically falls back to pure guidance mode.

## Installation

```
openclaw skills install @durenzidu/powpow-register
```

## Features

1. **Product intro**: ~120-character opening + UI screenshots bundled inside the skill
   (6 images in `assets/screenshots/`: map page, post detail page, etc.; send 1–3 depending on the scenario — no external image hosting, works offline).
2. **Assisted registration**: the agent proactively suggests username/nickname, offers a password choice (user-provided or agent-generated),
   sends and submits the verification code, uploads the avatar directly (≤5MB, non-SVG), and handles common errors automatically (taken/expired/rate-limited).
3. **One-click login (dual links)**: right after successful registration, a login link lands the user directly on the home page (during the free testing period, one click and it's usable);
   if it lands on the subscription page (testing period over) or the user wants to upgrade, follow the subscription flow — after payment arrives, a fresh login state is exchanged and the full-membership link lands them on the home page
   (via the platform's official `me?token=` bridge, which plants the HttpOnly cookie automatically).
4. **Subscription payment**: both Alipay (monthly ¥6.99 / quarterly ¥19.99 / yearly ¥69.99,
   one-time purchase, no auto-renewal) and PayPal (Premium Monthly, about $1/month, auto-renews, cancel anytime) are handled by the agent with order creation + arrival polling; WeChat QR code / Huawei IAP are pointed to.
5. **Error troubleshooting**: verification code not received, username/email taken, 403 not activated, account locked and other
   common issues — all taken from the platform source code with citations.

## File Structure

```
powpow-register/
├── SKILL.md                            # Main guidance (triggers, 8-step flow, tone rules, hard rules)
├── README.md
├── .clawhubignore
├── assets/
│   └── screenshots/                    # Bundled product screenshots (powpow-01~06.jpg)
├── scripts/
│   └── powpow-register.mjs             # Core script (zero-dependency Node≥18, 11 subcommands)
└── references/
    ├── agent-flow.md                   # Script contract, full sequence, dual-link mechanism, security design
    ├── registration-flow.md            # Field rules, rate limits, error lookup table (with source citations)
    ├── payment-and-activation.md       # Alipay vibepay contract, activation chain, channel troubleshooting
    └── screenshots.md                  # Bundled screenshot list + scenario quick reference
```

## Security

- **The password** is passed into the script process only via an environment variable — never as a command-line argument, never written to disk, never stored in the state file;
  an agent-generated password is shown once for the user to save.
- **The verification code** is used only for the official registration API and discarded after use; the state file (email/username/token/order number)
  lives in the system temp directory and is removed with one `cleanup` at the end of the flow.
- **Payment**: the agent only creates orders, opens the cashier and queries arrival; it never touches the user's Alipay/PayPal account
  or payment credentials, and never pays on their behalf. Payment always happens between the user and the official cashier.
- All requests go to the official domain `https://global.powpow.online` only; contains no secrets.

## License

MIT-0 (unified ClawHub license).

## Links

- Official site: https://global.powpow.online
- Registration: https://global.powpow.online/register
- Learn about Bubble (video): https://www.bilibili.com/video/BV1Wu826UEVz/
