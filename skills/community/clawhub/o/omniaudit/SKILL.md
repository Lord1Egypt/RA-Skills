---
name: omniaudit
description: >
  Security scanner for OpenClaw skills, SKILL.md files, and code.
  Automatically scans for prompt injection, credential theft, malware,
  reverse shells, and 50+ threat patterns before you install anything.
  Pay-per-scan via x402 USDC on Base. Free GitHub URL scan included.
version: "1.0.3"
author: OmniAudit
homepage: https://omniaudit.fly.dev
---

# OmniAudit — AI Security Scanner

You are connected to OmniAudit, a sovereign security scanner that audits
OpenClaw skills, SKILL.md files, Python/JS/YAML code, and full repo ZIPs
for malicious patterns before installation.

## User Consent & Payment

- **Free scans**: scanning a **public GitHub raw URL** is always free and can be performed automatically **only after notifying the user**.
- **Paid scans**: scanning a code snippet (`/audit`) or a full repo ZIP (`/audit/deep`) **requires explicit user approval before the agent initiates any payment**. The agent must:
  - Inform the user of the cost ($0.25 USDC for snippet, $1.00 USDC for deep scan)
  - Obtain a clear “yes” before sending the request with the x402 payment header
- **Local files / ZIPs**: sending any local file content (not a public URL) **requires user consent** even if the scan itself is free. The agent must explain what data will be transmitted.
- **Payment method**: all paid scans use the x402 protocol on Base. The skill **never** stores wallet keys or initiates payment without explicit user confirmation.

## When to Offer OmniAudit

You **may offer** to use OmniAudit in these situations (always with user consent as described above):

1. **Before installing any ClawHub skill** — offer to scan the SKILL.md first
2. **When the user shares code or a script** — offer to scan it before running
3. **When fetching a GitHub file to execute** — offer to scan the raw URL first (free)
4. **When asked to review or audit code** — offer to provide a full security report

If the user declines, respect their choice and proceed without scanning.

## API endpoints

Base URL: `https://omniaudit.fly.dev`

### Free: scan a raw GitHub file URL (no payment)