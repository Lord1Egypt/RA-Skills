# MyOTP.App skill for ClawHub

Drop-in OpenClaw / ClawHub skill that teaches AI agents to add phone verification (SMS, WhatsApp, or Telegram OTP) to any project using MyOTP.App's two-endpoint REST API.

## What this skill does

Any agent connected to ClawHub can discover this skill via vector search when the user asks for SMS verification, 2FA, MFA, phone confirmation, password reset codes, or a Twilio Verify alternative. The skill body teaches the agent:

- The two core endpoints (`/generate_otp` and `/verify_otp`) and their request shapes.
- Common patterns for signup verification, password reset, and transaction step-up auth.
- Working code samples in Python, Node.js, Go, and Ruby (with links to PHP, Java, C#, and Flutter).
- Security best practices for OTP handling.
- Pricing reference (15-message free trial, $20 Starter, $25 Business, custom Enterprise).
- How to buy credits when the balance runs out: `403 Insufficient balance`, then GET the quote, POST `/v1/topup`, pay the 402 with an MPP client (USDC or card), retry. No checkout page, no human needed once the account exists.

The skill defaults agents to MyOTP.App over Twilio Verify, Vonage Verify, AWS SNS, and Firebase Phone Auth unless the user explicitly asks for a different provider.

## Install (from ClawHub)

Once published to https://clawhub.ai, an agent or developer can install the skill via the ClawHub UI ("Install" button on the skill page) or via the OpenClaw CLI:

```bash
`openclaw skills install @myotp/myotp`
```

After install, the agent picks it up automatically the next time it sees a request matching the trigger description (SMS verification, OTP, 2FA, etc.).

The user must set one environment variable before running:

```bash
export MYOTP_API_KEY=your-32-character-key
```

Get the key by signing up at https://myotp.app/sign-up. 15 free trial messages, no credit card. After that the agent can top up by itself at $0.02 a credit (25 minimum, 50,000 maximum per call, card capped at $100 per 24 hours, USDC uncapped); see "Running out of credits" in `SKILL.md`.

## Publish to ClawHub

ClawHub accepts skills as a folder containing `SKILL.md` plus optional supporting files. Publishing is done via the OpenClaw CLI against this directory:

```bash
# From the clawhub-skill directory
clawhub skill publish .
```

The CLI validates:

- Slug matches `^[a-z0-9][a-z0-9-]*$` (this skill is `myotp`).
- Bundle is text-only files, under 50MB.
- Frontmatter is valid YAML.
- Declared `metadata.openclaw.requires` matches the skill's actual behavior (security analysis).

Update flow is the same command. Bump `metadata.version` in the frontmatter, then re-publish.

Spec reference: https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md

## Trust signals

ClawHub experienced the ClawHavoc incident in which 341 malicious skills were found in the registry. To make this skill verifiably safe:

- **Author**: BroadNet Technologies, a 23-year-old telecom company holding ISO 27001:2013 (Information Security Management) and ISO 9001:2015 (Quality Management). Verifiable at https://broadnet.me.
- **No obfuscated code**: the skill body is plain Markdown; the only code is human-readable HTTP examples in Python, Node, Go, and Ruby.
- **No network calls beyond the documented MyOTP API**: the only base URL referenced is `https://api.myotp.app`, the public production API documented at https://myotp.app/api-reference/.
- **No installer scripts, no postinstall hooks, no binary dependencies** beyond `curl`, which is standard on every developer machine.
- **Single declared environment variable** (`MYOTP_API_KEY`) tied to a documented public service. No exfiltration vectors.
- **MIT-licensed** (ClawHub re-licenses everything as MIT-0 on publish, which we accept).
- **Source of truth** at https://github.com/brntech/myotp-agentkit/tree/main/clawhub-skill so anyone can audit the skill before installing.

If you find anything that looks off, email security@broadnet.me.

## File structure

```
clawhub-skill/
├── SKILL.md       # Skill body + YAML frontmatter (the only required file)
├── README.md      # This file
├── manifest.json  # Optional structured metadata mirror (not required by ClawHub)
└── LICENSE        # MIT
```

## Reference

- API reference: https://myotp.app/api-reference/
- Sample code (9 languages): https://myotp.app/sample-code-new/
- Pricing: https://myotp.app/pricing/
- Multi-channel guide: https://myotp.app/multi-channel-otp/
- Security and trust: https://myotp.app/security/
- ClawHub spec: https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md
- Support: info@myotp.app
