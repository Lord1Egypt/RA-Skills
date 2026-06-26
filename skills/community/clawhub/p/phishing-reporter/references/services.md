# Reporting Services Reference

## 1. Google Safe Browsing (Primary)
- **URL**: https://safebrowsing.google.com/safebrowsing/report_phish/?hl=en
- **Method**: Browser automation (form fill + submit)
- **CAPTCHA**: reCAPTCHA v3 (invisible, usually passes)
- **Success indicator**: "Submission was successful." message
- **Impact**: Blocks site in Chrome, Firefox, Safari, Android

### Threat Types
| Type | When to use |
|------|-------------|
| Social Engineering | Phishing, scams, fake login pages |
| Malware | Sites distributing malicious software |
| Unwanted Software | Sites pushing unwanted browser extensions, toolbars |

### Threat Categories (Social Engineering only)
| Category | Examples |
|----------|----------|
| Bank / Financial Phishing | Fake bank logins, payment portals |
| Crypto Exchange Phishing | Fake Binance, Coinbase, etc. |
| Social Media Platform Phishing | Fake Facebook, Instagram logins |
| Retail Phishing | Fake Amazon, eBay, shop pages |
| Email Provider Phishing | Fake Gmail, Outlook logins |
| Entertainment Phishing | Fake Netflix, Spotify, gaming |
| Government Agency Phishing | Fake tax, immigration, ID portals |
| Package Tracking Scam | Fake DHL, Post, FedEx tracking |
| Fake Support Scam | Fake Microsoft/Apple support |
| Government Fines Scam | Fake traffic tickets, tax fines |
| Fake Prize/Giveaway Scam | "You won!" scams |
| Other Phishing | Anything else phishing |
| Other Scam | Anything else scam |

## 2. NCSC Switzerland (Swiss National Cyber Security Centre)
- **URL**: https://www.report.ncsc.admin.ch/en/
- **Method**: Browser automation (multi-step chat wizard)
- **CAPTCHA**: None
- **Type**: Chat-based wizard with multiple selections
- **Email alternative**: notification@ncsc.ch
- **Impact**: Swiss authorities investigate, may contact hosting provider

### Chat Wizard Path (Phishing Website)
```
Step 1: "I want to report a cyber-incident voluntarily"
Step 2: "A website/a web service/a web platform"
Step 3: "I would like to report a third-party website"
Step 4: "The website displays fraudulent content"
Step 5: "The website copies another known website"
Step 6: Enter URL and details
Step 7: Submit
```

### Direct Path URLs
- Start: `https://www.report.ncsc.admin.ch/en/chat?path=406%3E407%3E1`
- After website selection: `https://www.report.ncsc.admin.ch/en/chat?path=406%3E407%3E1%3E128%3E132%3E133%3E314`
- After third-party + fraudulent: `https://www.report.ncsc.admin.ch/en/chat?path=406%3E407%3E1%3E128%3E132%3E133%3E314%3E130%3E135`

## 3. Cloudflare Abuse
- **URL**: https://abuse.cloudflare.com/phishing
- **Method**: Browser automation (less reliable)
- **CAPTCHA**: Turnstile (visible, often blocks bots)
- **Fallback**: Provide manual instructions
- **When**: Only if site is behind Cloudflare (check DNS)

## 4. PhishTank (Community)
- **URL**: https://phishtank.org/
- **Method**: Requires account registration
- **Note**: Good community-driven database

## 5. APWG (Email-based)
- **Email**: reportphishing@apwg.org
- **Method**: Forward phishing email or describe URL
- **Note**: Anti-Phishing Working Group, industry consortium

## 6. Domain Registrar
- **Method**: WHOIS lookup → find abuse contact → send email
- **Tool**: `whois <domain>` or https://who.is/<domain>
- **Template**: Include phishing URL, what it impersonates, screenshots if possible
