---
name: url-safety-triage
description: |
  Decide whether a link is safe to open, click or pay before an agent follows it. Checks two phishing
  blocklists on every redirect hop, the destination domain's age and trust flags, HTTPS and security
  headers, and named look-alike tricks, returning one overall risk verdict.

  USE FOR:
  - Vetting a link found in an email, chat message, scraped page or tool result before opening it
  - Checking a payment or checkout URL for phishing and look-alike domains
  - Explaining why a link was judged risky, with the exact signals

  TRIGGERS:
  - "is this link safe", "check this URL", "phishing check", "url safety"
  - "before you click / open / pay this link"
  Sold as x402/MPP pay-per-call tools on Base and Solana; agents pay per successful call.
metadata:
  version: 1
---

# URL safety triage

One call, $0.02, no account. Failed calls are not charged.

| Task | Endpoint | Price |
|------|----------|-------|
| Full link verdict | `https://api.glyphcall.com/pack/url-safety?url=<full-url>` | $0.02 |
| Blocklist only | `https://api.glyphcall.com/phishing/check?url=<full-url>` | $0.01 |

Use the agentcash client so payment and retries are handled:

```sh
npx agentcash@latest check "https://api.glyphcall.com/pack/url-safety?url=https%3A%2F%2Fexample.com"
npx agentcash@latest fetch "https://api.glyphcall.com/pack/url-safety?url=https%3A%2F%2Fexample.com"
```

The result contains `risk` (`low`, `medium`, `high`), the blocklist matches per host, the redirect
chain, the domain age and trust flags, and named signals (new domain, bare IP, punycode look-alike,
`user@host` trick). When every check fails and nothing could be verified, treat the verdict as
unknown rather than safe.

