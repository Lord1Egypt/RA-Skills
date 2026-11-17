---
name: lygo-site-card
description: "LYGO Site Card — turn a public HTTPS URL or local HTML file into a compact identity card: title, description, canonical, security headers, security.txt/robots companions, SHA-256, yield ALIGNED/DRIFT/SHADOW. Use when checking if a page is live, comparing two URLs, verifying CSP/HSTS, site card, link passport, public page pulse, or /lygo-site-card. HTTPS GET only; no POST; no subprocess; no live Star Chart write."
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "🪪"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-site-card"
    requires:
      anyBins: [python, python3]
  lygo: true
  site_card: true
  signature: "Delta9Phi963-SITE-CARD-v1.0.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/lygo-site-card"
  permissions:
    network:
      https_get: "user-supplied URL; HTTPS + public IP only"
      http_post: false
    filesystem:
      read: "optional --file HTML"
      write: "opt-in --write with --i-consent"
    shell: false
    subprocess: false
    publish: false
    live_star_chart: false
---

# LYGO Site Card v1.0.0 🪪

**One GET. One card. Empty is honest.**

A compact public identity card for a URL (or a local HTML file): title, description, canonical, security headers, `security.txt` / `robots.txt`, body SHA-256, yield **ALIGNED / DRIFT / SHADOW**.

**Signature:** `Delta9Phi963-SITE-CARD-v1.0.0`  
**ClawHub:** `npx clawhub@latest install deepseekoracle/lygo-site-card`

This is not Palantir, not a crawler farm, not a live Star Chart write.

---

## When to use

- “Is this page live?” / “Does it have CSP?” / “site card” / “link passport”
- Compare staging vs production (`compare`)
- Agents verifying GitHub Pages / HF Spaces / lattice limbs after a deploy
- Local HTML parse with `--file` (no network)

## When NOT to use

- Private/internal hosts (blocked: loopback, RFC1918, link-local)
- `http://` (HTTPS only)
- Scanning other people’s private apps
- Auto git / HF / ClawHub / social publish

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-site-card
cd path/to/lygo-site-card
python scripts/self_check.py
```

---

## Commands

```bash
python scripts/site_card.py card https://chatagent.ca/lattice/
python scripts/site_card.py card --file ./index.html
python scripts/site_card.py headers https://chatagent.ca/lattice/
python scripts/site_card.py compare https://chatagent.ca/lattice/ https://eternalhaven.ca/lattice/
python scripts/site_card.py card https://chatagent.ca/lattice/ --write card.json --i-consent
```

| Command | Network | Disk |
|---------|---------|------|
| `card URL` | HTTPS GET page + optional companions | none unless `--write --i-consent` |
| `card --file` | none | read HTML |
| `headers URL` | HTTPS GET | optional write |
| `compare A B` | two GETs | optional write |

---

## Yield

| Yield | Meaning |
|-------|---------|
| **ALIGNED** | HTTP 200, a title, and CSP **or** Referrer-Policy present |
| **DRIFT** | Live but missing title or security headers |
| **SHADOW** | GET failed, blocked host, or non-HTTPS |

Missing companions (`security.txt`, `robots.txt`) stay **named** on the card. They do not invent a policy.

---

## Safety

- HTTPS only; no userinfo in URLs; no private IPs; redirects re-checked
- No subprocess / shell / POST
- Writes require `--i-consent`
- Body capped at 400 KB

Read `references/SECURITY.md`.

---

## Pair with

| Skill | Role |
|-------|------|
| `lygo-public-witness` | Globe overlay; this skill is the per-URL card |
| `lygo-skill-spector` | Scan a skill folder, not a website |
| `lygo-flame-ward` | Discourse ingest, not HTTP headers |
| `lygo-mint-verifier` | Hash a pack; this hashes a page body |

---

## License

**MIT-0** (see `LICENSE`).  
**Δ9Φ963 — one GET · one card · human remains the publisher.**
