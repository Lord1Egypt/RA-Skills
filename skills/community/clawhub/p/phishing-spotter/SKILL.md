---
name: phishing-spotter
description: "Use when you receive a suspicious email, SMS, or voice-mail attempt and want to know if it's phishing BEFORE clicking — parses raw message text or .eml files, extracts URLs and analyzes them character-by-character (homograph IDN tricks, subdomain brand spoofing, URL shorteners, punycode, credential-path patterns like /login/verify), checks 25+ social-engineering pressure patterns (urgency, fear, authority, curiosity, authority), scores the message 0-100, and explains each signal in plain language so you learn to spot the next one yourself."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [phishing, security, email, scams, fraud-prevention, education]
---

# Phishing Spotter

## Overview

Phishing is still how most accounts get hijacked — not zero-days, not genius hacking, just a message that looks like it's from your bank. AI has made these dramatically better: perfect grammar, tailored context, convincing sender names. The weakest link is the three seconds between "Your account will be suspended" and the click.

This skill is a **train-your-instincts analyzer**. It doesn't just say "dangerous" — it shows you every signal in the message, weighted, explained, so the analysis doubles as education. Run it on messages you're unsure about; after a dozen, you start seeing the patterns yourself.

What it checks:

1. **URL forensics** — extracts every URL and dissects it: homograph/IDN character tricks (`pаypal.com` with a Cyrillic а), brand names in subdomains (`paypal.com.evil.io`), URL shorteners, punycode (`xn--`), IP-address hosts, credential-bait paths (`/login`, `/verify`, `/wallet`), lookalike TLDs (`.co`, `.tk`, `.xyz`), `@` trickery in URLs, hex/redirect chains.
2. **Social-engineering patterns** — 25+ pressure tactics: artificial urgency, fear consequences, authority invocation, curiosity gaps, too-good-to-be-true offers, secrecy requests, unusual payment rails (gift cards, crypto, wire).
3. **Structural tells** — mismatched display-name vs domain, no personalization, generic greetings, reply-to divergence, attachment-type risk.
4. **Plain-language report** — every signal explained with the actual matched text, a 0–100 risk score with verdict band, and the two or three things to check before acting.

Offline, stdlib-only. No URLs are visited — analysis is purely textual, so running it never tips off an attacker.

## When to Use

- **"Is this email real?"** — the core use: bank/employer/delivery/government impersonation.
- **Analyze before forwarding** — check a suspicious message before sending it to family or IT (and strip URLs when forwarding).
- **Training family members** — run it on real examples together; the explanations are the curriculum.
- **SMS/smishing and voice vishing scripts** — paste the text; same pressure-pattern engine.
- **Security awareness for small teams** — score a sample of reported emails, discuss signals.
- Don't use for: actually visiting suspected phishing links (never), messages that are clearly abusive/threatening (contact authorities), or as the sole gate for enterprise mail security (use real mail security tooling).

## How It Works

1. **Get the raw text** — paste the body, or better, the full .eml (headers included: `From:`, `Reply-To`, `Subject` get extra checks).
2. **Extract artifacts** — URLs, email addresses, domains, phone numbers, attachment names.
3. **Run detectors** — URL forensics + pressure patterns + structural tells; each match contributes weighted points.
4. **Score & explain** — 0–100 with band: 0–24 LOW / 25–49 SUSPICIOUS / 50–74 LIKELY PHISHING / 75+ ALMOST CERTAINLY PHISHING. Every point of score is tied to a quoted match and explanation.
5. **Learn** — the report ends with "signals to memorize" — the top 3 signals from THIS message.

## Commands

```bash
# Analyze pasted text (body only)
python3 scripts/phishing_spotter.py analyze message.txt

# Analyze a full .eml with headers (more detectors fire)
python3 scripts/phishing_spotter.py analyze suspicious.eml

# Just dissect a URL you're unsure about
python3 scripts/phishing_spotter.py url "http://paypal.com.verify-account.io/login"

# List all pressure-pattern detectors
python3 scripts/phishing_spotter.py list-patterns

# JSON for pipelines
python3 scripts/phishing_spotter.py analyze message.txt --json
```

## Example Session

```
$ python3 scripts/phishing_spotter.py analyze references/sample-phish.txt

RISK SCORE: 87/100 — ALMOST CERTAINLY PHISHING
Based on 11 signals. Do not click, do not reply.

TOP SIGNALS:
[+25] BRAND IN SUBDOMAIN SPOOF
  URL: http://paypal.com.verify-account.io/login
  The real brand is in a SUBDOMAIN. Reading right-to-left: the actual
  site is verify-account.io. paypal.com belongs to the attacker's
  subdomain string, not to PayPal.

[+20] CREDENTIAL-BAIT PATH
  /login in URL path — phishing kits love paths that promise a login
  form. Combined with brand spoofing above, this is a credential
  harvester with near-certainty.

[+15] ARTIFICIAL DEADLINE
  "within 24 hours" — real institutions send notice before action,
  not countdown ultimatums. Urgency exists to stop you thinking.

[+12] THREAT OF ACCOUNT LOSS
  "your account will be permanently suspended" — fear of loss is the
  #1 phishing motivator. Banks don't suspend accounts by email.

URL ANALYSIS:
  1. http://paypal.com.verify-account.io/login
     host=verify-account.io  ← BRAND 'paypal' IN SUBDOMAIN (spoof)
     path contains credential bait: /login
  2. https://bit.ly/3xKp2mQ
     shortener — destination hidden; expand (safely) before any trust

STRUCTURAL TELLS:
  Display name "PayPal Support" vs domain verify-account.io — mismatch

BEFORE YOU ACT — verify independently:
  1. Open your bank's app/site directly (type it yourself). Any real
     "suspicious activity" notice will be visible there too.
  2. If unsure, call the number ON YOUR CARD, never one from the message.
  3. Report: forward to phishing@<brand-domain> and delete.

SIGNALS TO MEMORIZE FROM THIS MESSAGE:
  1. Brand in subdomain (paypal.com.evil.io) — read domains right-to-left
  2. 24-hour ultimatums
  3. Display name ≠ sending domain
```

## Detector Reference (abridged)

| Category | Detectors | Weight |
|---|---|---|
| URL spoofing | homograph/IDN chars, brand-in-subdomain, `@` in URL, punycode `xn--`, IP host, lookalike TLD | 20–25 |
| URL infrastructure | shorteners, credential-bait paths, hex-encoded hosts, double redirects | 8–20 |
| Pressure tactics | artificial deadline, account-loss threat, legal action, authority claim, curiosity gap, lottery/reply-too-good | 10–15 |
| Payment rails | gift cards, crypto wallets, wire instructions, "pay to release" | 12–15 |
| Structural | display-name mismatch, reply-to divergence, generic greeting, no personalization, risky attachment ext | 5–12 |

Full pattern list: `list-patterns`.

## Workflow for an Agent

1. Never visit extracted URLs. All analysis is textual — keep it that way.
2. Ask for the rawest form available (.eml > pasted body > screenshot OCR).
3. Run `analyze`; present score, then the TOP signals with quotes — the quoted text IS the evidence.
4. End with the verify-independently steps (app-first, card-back number, report addresses).
5. If the user already clicked: pivot to damage control — password resets, session revocation, bank notification, credit freeze. Speed matters more than analysis then.

## Common Pitfalls

1. **Visiting the link "to check".** That's the phishing test failing in real time. Analysis here never fetches.
2. **Trusting a padlock/HTTPS.** Half of phishing sites have valid TLS. The report ignores the scheme for scoring (except http:// plain on a "bank" — extra suspicious).
3. **Score worship.** A 22 can still be phishing (sophisticated, tailored lures score low); a 55 can be a clumsy legit marketing mail. Read the signals, not just the number.
4. **Matching brand names naively.** `paypal.com.verify-account.io` contains "paypal.com" as a substring — that's the trick. Detectors parse domain structure, not substrings.
5. **Forgetting SMS/voice.** The pressure patterns apply to smishing texts and vishing call scripts; paste those too.
6. **Replying to ask "is this real?".** Replying confirms a live target and invites escalation. Report-and-delete instead.

## Verification Checklist

- [ ] Message analyzed from the rawest available form (headers if possible)
- [ ] Score presented with band AND the individual quoted signals
- [ ] Every URL dissected with the actual registrable domain identified
- [ ] Verify-independently steps included (app-first, card-back number)
- [ ] If already clicked: damage-control steps given before analysis
- [ ] Nothing was fetched — analysis stayed purely textual
