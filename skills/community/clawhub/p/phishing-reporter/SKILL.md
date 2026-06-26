---
name: phishing-reporter
description: Report phishing, malware, and scam URLs to Google Safe Browsing, NCSC (Swiss Cyber Security), and other abuse reporting services. Use when a user shares a suspicious/phishing URL and wants it reported, or asks to report a dangerous website. Triggers on phrases like "report phishing", "melde diese Seite", "report this URL", "phishing melden", "scam melden", "report abuse".
---

# Phishing Reporter

Report dangerous URLs to abuse/safety services via browser automation.

## Reporting Strategy

Report to **all applicable services** in order:

1. **Google Safe Browsing** (automated) — global reach, blocks in Chrome/Firefox/Safari
2. **NCSC Switzerland** (semi-automated) — Swiss national cyber security centre
3. **Domain registrar** (manual) — WHOIS lookup → abuse contact

## Service 1: Google Safe Browsing (fully automated)

**URL**: `https://safebrowsing.google.com/safebrowsing/report_phish/?hl=en`

### Workflow

Use the browser tool (profile: `openclaw`) to automate:

1. Open the URL above
2. Report Type: "This page is not safe" (default, leave as-is)
3. Click "Threat Type" dropdown → select "Social Engineering" (for phishing)
4. Click "Threat Category" dropdown → select best match (see references/services.md)
5. Click URL textbox → type the phishing URL
6. Click Additional details textbox → type description
7. Click Submit
8. Verify "Submission was successful" message

### Notes
- Form uses custom dropdowns: click combobox → click option in listbox
- reCAPTCHA v3 runs invisibly — usually passes for headless browsers
- If CAPTCHA blocks: provide manual instructions as fallback

## Service 2: NCSC Switzerland (chat wizard)

**URL**: `https://www.report.ncsc.admin.ch/en/`

The NCSC uses a **multi-step chat wizard** (not a simple form). Automate via browser:

### Chat Path for Phishing Website Reports

1. Open `https://www.report.ncsc.admin.ch/en/chat?path=406%3E407%3E1`
2. Click: **"A website/a web service/a web platform"**
3. Click: **"I would like to report a third-party website"**
4. Click: **"The website displays fraudulent content"**
5. Click: **"The website copies another known website"** (for phishing clones)
6. Continue through remaining steps (URL input, description, contact info)
7. Submit the report

### Direct Path URL (skips first steps)
```
https://www.report.ncsc.admin.ch/en/chat?path=406%3E407%3E1%3E128%3E132%3E133%3E314%3E130%3E135
```

### Notes
- Wizard is stateful — each step reveals the next
- No CAPTCHA, but many clicks required
- Email alternative: `notification@ncsc.ch` (include URL and description)
- If automation fails, provide the direct path URL + instructions

## Service 3: Domain Registrar (manual lookup)

1. Run WHOIS lookup: `whois <domain>` or use `https://who.is/<domain>`
2. Find "Registrar Abuse Contact Email"
3. Send abuse email with phishing URL and description

## Additional Details Template

```
Phishing site impersonating [BRAND]. Domain mimics [REAL SERVICE] customer service.
Designed to steal [banking credentials / login data / personal information].
```

## Fallback: Manual Instructions

If automated submission fails, provide the user with:
1. Direct links to each reporting form
2. The URL to report
3. Recommended categories/types
4. Pre-written description text

## Additional Reporting Services

See `references/services.md` for full list including Cloudflare, PhishTank, and APWG.
