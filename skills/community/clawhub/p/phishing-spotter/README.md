# Phishing Spotter

**"Is this email real?" — analyzed in seconds, with reasons you can learn from.**

Phishing remains the #1 way accounts get hijacked — not exotic hacking, just
a convincing message. AI has supercharged it: flawless grammar, perfect
formatting, tailored context. Every inbox, every family group chat, every
company has that moment: *this looks official… but is it?*

Phishing Spotter dissects the message **textually** — it never visits any
link — and shows you every signal, weighted and explained:

- **URL forensics** — brand-in-subdomain spoofs (`paypal.com.evil.io`),
  homograph attacks (Cyrillic а in `pаypal.com`), punycode (`xn--`),
  `@`-tricks, shorteners, IP hosts, credential-bait paths
- **25+ pressure patterns** — artificial deadlines, account-loss threats,
  legal threats, gift-card/crypto/wire payment rails, OTP requests,
  romance-scam phrasing, BEC "our bank details changed", missed-delivery
  smishing, tech-support scares
- **Structural tells** — Reply-To divergence, display-name impersonation,
  generic greetings, risky attachment types
- **0–100 score with band** + quoted evidence for every point
- **Verification steps + "signals to memorize"** — the analysis doubles as
  training, so you need the tool less over time

Works on email, SMS (smishing), and voice scripts (vishing) — any text.
Calibration: classic PayPal spoof → **100/100**; genuine GitHub security
alert → **24/100 (LOW)**.

## Quick Start

```bash
# Analyze a pasted message or full .eml (headers enable more detectors)
python3 scripts/phishing_spotter.py analyze suspicious.eml

# Dissect a single URL
python3 scripts/phishing_spotter.py url "http://paypal.com.verify-account.io/login"

# See the full pattern library
python3 scripts/phishing_spotter.py list-patterns
```

## Example Output

```
RISK SCORE: 100/100 — ALMOST CERTAINLY PHISHING

[+25] BRAND_SUBDOMAIN
  Evidence: "http://paypal.com.verify-account.io/login"
  'paypal' appears in the host but the actual site is
  'verify-account.io'. Read domains right-to-left.

[+15] DEADLINE — "within 24" hours
[+12] ACCOUNT_LOSS — "permanently suspended"
[+12] REPLY_TO_DIVERGENCE — replies go to mail-secure-net.tk
```

## Safety Model

- **Never fetches** — analysis is purely textual; running it can't tip off
  the attacker or load tracking pixels.
- **Ignores the padlock** — HTTPS proves nothing; free certs are universal.
- Score is evidence-weighting, not proof — sophisticated low-noise lures can
  score LOW, which is why every report ends with independent verification
  steps (open the app yourself, call the number on your card).

## If You Already Clicked

`references/signal-reference.md` ends with a 7-step damage-control order
(disconnect → reset password from another device → revoke sessions → bank →
check mail forward rules → report).

## License

MIT — see [LICENSE](LICENSE). Sample phish in `references/` is synthetic.
