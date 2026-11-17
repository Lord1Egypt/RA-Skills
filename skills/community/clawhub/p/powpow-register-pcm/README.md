# powpow-register

PowPow Bubble registration helper (OpenClaw version): carry one new user from "e no know wetin Bubble be" go reach "account don activate, one-click login, start to play" — product intro (with interface screenshots), registration wey agent go do (including avatar upload), Alipay/PayPal subscription order and money-landing tracking, one-click login with two links, error troubleshooting.

**Since v2.0.0 dis one na agent-helper mode, and since v2.2.0 e dey adapt to di platform free testing period**: di core script `scripts/powpow-register.mjs` na zero-dependency
(Node ≥ 18); di user dey comot from di conversation only once: to check di verification code for inbox. During di current free testing period, account wey don register fit use every feature at once — subscription payment na optional upgrade; if di testing period end and di user land for di subscription page, di flow dey switch to di payment path by imself. Without Node, or wen di user prefer to do am by imself, e dey fall back by imself to pure guidance mode.

## Installation

```
openclaw skills install @durenzidu/powpow-register
```

## Features

1. **Product intro**: about 120 words opening + interface screenshots wey dey inside di package (`assets/screenshots/` get 6 pictures under am: map page, post detail page etc., choose 1–3 to send based on di situation; no need external image host, e dey work offline).
2. **Do-am registration**: agent go suggest username/nickname by imsef, password choose one of two (user provide am or agent generate am), send and submit di verification code, avatar direct upload (<=5MB no be SVG), common errors dem dey handle automatic (don dey take/don expire/rate limit).
3. **One-click login (dual links)**: right after registration succeed, login link dey land di user directly for di home page (during di free testing period, one click and e dey usable);
   if e land for di subscription page (testing period over) or di user want to upgrade, follow di subscription flow — after payment arrive, fresh login state dey exchange and di full-membership link land am for di home page
   (via di platform official `me?token=` bridge, wey dey plant di HttpOnly cookie automatically).
4. **Subscription payment**: both Alipay (monthly ¥6.99 / quarterly ¥19.99 / yearly ¥69.99, one-time buy no auto-renew) and PayPal (Premium Monthly, about $1/month, auto-renew, cancel anytime) na di agent go create order + poll money landing; overseas users fall back to PayPal; WeChat scan code/Huawei IAP just point di way.
5. **Error troubleshooting**: verification code no dey come, username/email don dey take, 403 no activate, account lock etc. common problems, all of dem come from platform source code with location mark.

## File structure

```
powpow-register/
├── SKILL.md                            # Main guide (trigger conditions, 8-step flow, tone rules, hard rules)
├── README.md
├── .clawhubignore
├── assets/
│   └── screenshots/                    # Product screenshots wey dey inside di package (powpow-01~06.jpg)
├── scripts/
│   └── powpow-register.mjs             # Main script (zero dependency Node>=18, 11 sub-commands)
└── references/
    ├── agent-flow.md                   # Script contract, full sequence, two-link mechanism, security design
    ├── registration-flow.md            # Field rules, rate limit, error troubleshooting table (with source code location)
    ├── payment-and-activation.md       # Alipay vibepay contract, activation chain, channel troubleshooting
    └── screenshots.md                  # Package screenshot list + scenario quick-find
```

## Security

- **Password** only enter di script process through environment variable, never write am inside command line argument, no store am on disk, no put am inside state file; password wey agent generate show once only so di user go save am.
- **Verification code** only dey use for di official registration endpoint, e dey throway once dem use am finish; di state file (email/username/token/order number) dey store for di system temporary directory, when di flow finish `cleanup` go clear am one click.
- **Payment**: agent only create order, open cashier, check money landing; never touch di user Alipay/PayPal account or payment credential, never pay for am. Payment always happen between di user and di official cashier.
- All requests dey go only to di official domain `https://global.powpow.online`; e no carry any key inside.

## License

MIT-0 (di unified ClawHub license).

## Links

- Official website: https://global.powpow.online
- Register: https://global.powpow.online/register
- Know Bubble (video): https://www.bilibili.com/video/BV1Wu826UEVz/
