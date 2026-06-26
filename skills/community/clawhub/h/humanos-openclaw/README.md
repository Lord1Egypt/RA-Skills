# Humanos — Human Approval for AI Agent Actions

An [OpenClaw](https://openclaw.ai) skill that gives AI agents the ability to request, verify, and enforce human authorization before performing sensitive operations.

When an agent needs to make a payment, sign a document, access personal data, or execute any high-stakes action, this skill sends a secure approval request to the right person. They review, approve or reject, and the result comes back as a [W3C Verifiable Credential](https://www.w3.org/TR/vc-data-model/) with cryptographic proof.

## Humanos - Programmable Human Authorization for Agent Actions

AI agents can execute actions.
Humanos lets them prove human authorization before they do.

Require a mandate signature before high-risk execution.

### What It Does

- Collect human approval before sensitive agent actions
- Issue machine-verifiable mandate signatures
- Support scoped delegation (amount, duration, action type)
- Enable revocation of previously granted authority

Humanos provides the authorization proof.
Your runtime decides whether to execute.

### When To Use It

Use Humanos when your agent can:

- Move money or sign transactions
- Initiate payouts, refunds, or batch payments
- Modify or delete user data
- Export or share sensitive data
- Change account permissions or roles
- Rotate API keys or security credentials
- Update billing details or subscription plans
- Execute contracts or legal agreements
- Accept updated terms on behalf of a user
- Grant third-party access to data
- Release funds from escrow
- Increase transaction or withdrawal limits
- File claims, applications, or regulatory forms
- Approve loan or credit changes
- Post or publish under a user's identity
- Control IoT or physical access devices
- Act on behalf of a user
- Delegate authority to another agent

If the action affects money, data, identity, ownership, or legal position, require a mandate signature.

### How It Works

1. Agent prepares a structured action
2. Agent calls `requestMandate(action, constraints)`
3. Human approves via SMS, email, wallet, API, or any programmable channel
4. Humanos returns a signed mandate signature
5. Agent verifies with `verifyMandate(signature)`
6. Agent decides whether to execute

No valid mandate signature -> execution should not proceed.

### Core API

`requestMandate(action, constraints) -> mandate_signature`
`verifyMandate(mandate_signature) -> true / false`
`revokeMandate(mandate_signature)`

Simple. Programmable. Deterministic.

### Built on Open Standards

Mandate signatures are issued as W3C Verifiable Credentials (VCs).

This makes them:

- Cryptographically verifiable
- Interoperable across systems
- Compatible with the EU Digital Identity Wallet
- Compatible with emerging agent payment protocols such as Google AP2

Human authorization becomes a portable, standards-based credential - not a platform-locked approval.

### Why Not Just Use Telegram?

Telegram gives you a chat confirmation.

Humanos gives you:

- Structured execution constraints
- Identity-bound authorization
- Machine-verifiable mandate signature
- Revocation support
- Reusable proof
- Standards-based verifiability (W3C VC)
- Built for agent systems, not chat logs

### What a Mandate Signature Can Represent

A mandate signature can represent:

- A simple yes/no approval
- A signed document (PDF)
- A payment authorization
- Identity verification (KYC)
- A structured form submission
- A multi-party approval

All exposed as a programmable verification call.

## Install

```bash
clawhub install humanos
```

Or install locally:

```bash
git clone https://github.com/Humanos-App/humanos-openclaw.git
cd humanos-openclaw
./scripts/setup-openclaw.sh
```

Manual setup:

```bash
ln -s $(pwd)/humanos-openclaw ~/.openclaw/skills/humanos
```

## Configure

1. Get an API key from [app.humanos.id](https://app.humanos.id)
2. Add credentials to `~/.openclaw/openclaw.json` and secure the file:

```json
{
  "skills": {
    "entries": {
      "humanos": {
        "enabled": true,
        "env": {
          "VIA_API_KEY": "your-api-key",
          "VIA_SIGNATURE_SECRET": "your-signing-secret"
        }
      }
    }
  }
}
```

```bash
chmod 600 ~/.openclaw/openclaw.json
```

3. Verify the skill loads:

```bash
openclaw skills list --eligible
```

## Usage

Talk to your OpenClaw agent naturally:

```
"I need approval from john@company.com to book a hotel for EUR 450"
"Send this NDA to partner@example.com for signing"
"Check if the approval request has been signed"
"Get consent from user@example.com for data processing"
"Cancel the pending approval request"
```

## First-run payload rules

To avoid generic `400 Bad Request` errors on create:

- Use `consent`, `json`, or `document` in `--type` (inline `form` is not supported).
- For `consent`, include a `text` field in `data`.
- For `document`, include a `pdf` field in `data` with base64 content.
- Keep `data` as an array of fields (`[{label,type,value,hidden}]`).

Example (`consent`):

```bash
./scripts/create-request.sh \
  --contact "+351919307983" \
  --type "consent" \
  --name "Football approval" \
  --data '[{"label":"text","type":"string","value":"I approve football tomorrow.","hidden":false}]'
```

## What It Does

| Operation | Description |
|-----------|-------------|
| **Create request** | Send approval request with OTP to a contact |
| **Check status** | Poll for PENDING / APPROVED / REJECTED |
| **Find requests** | Search by contact, DID, or internal ID |
| **Get credential** | Retrieve signed W3C Verifiable Credential with proofs |
| **Get mandate** | Check mandate scope, validity, and constraints |
| **Resolve DID** | Look up DID Document with verification methods |
| **Cancel request** | Revoke a pending approval |
| **Resend OTP** | Re-send verification code |

## Credential Types

| Type | What the person sees |
|------|---------------------|
| `document` | PDF to review and sign with drawn signature |
| `form` | Dynamic form with fields to fill |
| `json` | Structured data to approve or reject |
| `consent` | Terms to read and accept |

## Security Levels

| Level | When to use |
|-------|------------|
| `CONTACT` | Low-risk: OTP verification only |
| `ORGANIZATION_KYC` | Medium-risk: organization-level identity check |
| `HUMANOS_KYC` | High-risk: full KYC with identity verification |

## How It Works

```
Agent needs approval
    |
    v
Create request ──> Person receives secure link
                        |
                        v
                   Enter OTP, review details
                        |
                   ┌────┴────┐
                   v         v
              APPROVED   REJECTED
                   |         |
                   v         v
           Agent proceeds   Agent stops
           with proof       and informs user
```

## Optional: Mandate Guard Hook

For automatic enforcement, install the included hook that intercepts tool calls and blocks unauthorized actions:

```bash
cp -r hooks/humanos-guard/ ~/.openclaw/hooks/humanos-guard
openclaw hooks enable humanos-guard
```

This listens for `tool.pre` events and blocks sensitive operations (payments, transfers, signing) unless a valid mandate exists.

## Testing

Run the built-in test suite:

```bash
# Offline argument validation tests (no API key needed)
./scripts/test-all.sh

# Full integration tests (requires API credentials)
VIA_API_KEY=your-key VIA_SIGNATURE_SECRET=your-secret ./scripts/test-all.sh
```

## Security

- All requests signed with HMAC-SHA256
- API keys read from environment variables at runtime, never hardcoded in scripts
- When using OpenClaw, credentials are managed via `~/.openclaw/openclaw.json` — set secure file permissions (`chmod 600 ~/.openclaw/openclaw.json`)
- W3C Verifiable Credentials with EdDSA proofs
- OTP verification for all approval flows
- Guard hook uses native fetch API (Node.js 18+), no shell command execution
- No application data is stored locally by this skill

## Regulatory Compliance

Mandate signatures are W3C Verifiable Credentials, enabling compliance with:

- **PSD2** — Strong Customer Authentication for payments
- **GDPR** — Verifiable consent for data processing
- **HIPAA** — Auditable authorization for healthcare data access
- **eIDAS** — Compatible with EU Digital Identity Wallet

## Requirements

- [OpenClaw](https://openclaw.ai) installed
- `curl`, `jq`, and `openssl` on PATH
- `node` 18+ on PATH (required for the optional guard hook)
- VIA Protocol API key from [app.humanos.id](https://app.humanos.id)
- Optional: `VIA_API_URL` only if you need a non-default API base URL

## Links

- [Humanos Dashboard](https://app.humanos.id)
- [API Documentation](https://humanos.mintlify.app/essentials/introduction)
- [OpenClaw](https://openclaw.ai)
- [ClawHub](https://clawhub.ai/lagosrui/humanos-openclaw)
- [VIA Protocol](https://github.com/Humanos-App/agent-mandate-protocol)

## License

MIT
