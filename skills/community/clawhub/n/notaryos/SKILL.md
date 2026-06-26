---
name: notaryos
description: Seal AI agent actions with Ed25519 cryptographic receipts. Verify what your agent did and prove what it chose not to do.
version: 2.4.0
metadata:
  openclaw:
    emoji: "\U0001F6E1\uFE0F"
    requires:
      bins:
        - python3
    primaryEnv: NOTARY_API_KEY
    homepage: https://github.com/hellothere012/notaryos
    files:
      - "sanitize.py"
    install:
      - kind: uv
        package: notaryos
        bins: []
---

# NotaryOS — Cryptographic Receipts for Agent Actions

Seal your agent's actions with Ed25519 signatures. Issue tamper-evident receipts, verify them publicly, and maintain an auditable chain of every decision.

## License

BSL-1.1 (Business Source License). See https://github.com/hellothere012/notaryos/blob/main/LICENSE

## Trust Statement

By using this skill, action metadata (action type, timestamps, and a SHA-256 hash of the payload) is sent to `api.agenttownsquare.com` via HTTPS. Raw payload retention depends on your tier — see the Data Flow section below. Verification is free and requires no account. Full privacy policy: https://notaryos.org/privacy

## Data Flow

The SDK sends your payload to the NotaryOS API via HTTPS POST. The server hashes the payload with SHA-256, signs the hash with Ed25519, and returns a receipt.

| Tier | Payload Transmitted | Raw Payload Retained | Hash Stored | Signature Stored |
|------|-------------------|---------------------|-------------|-----------------|
| Demo (no key) | Yes | No | Yes | Yes |
| Free | Yes | Metadata only | Yes | Yes |
| Pro | Yes | Configurable | Yes | Yes |
| Enterprise | Yes | Zero retention | Yes | Yes |

The included `sanitize.py` module strips fields matching known sensitive patterns before transmission. Use it before every `seal()` call when handling user data.

## External Endpoints

| URL | Method | Data Sent | Purpose |
|-----|--------|-----------|---------|
| `api.agenttownsquare.com/v1/notary/issue` | POST | action_type, payload JSON | Issue signed receipt |
| `api.agenttownsquare.com/v1/notary/verify` | POST | receipt JSON | Verify signature |
| `api.agenttownsquare.com/v1/notary/status` | GET | None | Health check |
| `api.agenttownsquare.com/v1/notary/r/{hash}` | GET | None | Receipt lookup |
| `api.agenttownsquare.com/v1/notary/public-key` | GET | None | Ed25519 public key |

No other endpoints are contacted. No telemetry, analytics, or tracking.

## Setup

```bash
pip install notaryos
```

> **No API key required.** The SDK auto-injects a free demo key (10 req/min) when `NOTARY_API_KEY` is not set. For production rates, get a key at https://notaryos.org/sign-up and set `NOTARY_API_KEY` in your environment or OpenClaw config.

```python
from notaryos import NotaryClient

notary = NotaryClient()  # works immediately — uses demo key if NOTARY_API_KEY is not set
```

## Seal an Action

```python
from notaryos import NotaryClient
from sanitize import sanitize_payload

notary = NotaryClient()

receipt = notary.seal(
    "file.created",
    sanitize_payload({
        "path": "/src/main.py",
        "lines_added": 42,
        "branch": "feature/auth"
    })
)

print(receipt.receipt_hash)
print(receipt.signature)
```

## What to Seal

### Default (always safe)

| Action Type | When to Seal |
|---|---|
| `file.created` | Created or modified a file |
| `file.deleted` | Deleted a file |
| `command.executed` | Ran a shell command |
| `config.changed` | Modified system configuration |

### Extended (sanitize payload first)

| Action Type | When to Seal |
|---|---|
| `email.sent` | Sent an email (strip body, keep subject) |
| `api.called` | Made an external API call (strip auth headers) |
| `data.accessed` | Accessed sensitive data (log access, not content) |
| `message.sent` | Sent a message (strip body if private) |

Always run `sanitize_payload()` on extended actions before sealing.

## Payload Guidelines

**Include:** File paths, counts, timestamps, branch names, public identifiers, action summaries.

**Exclude:** Authentication credentials, financial numbers, government IDs, message bodies, file contents, health information. The `sanitize_payload()` helper handles this automatically.

## Verify a Receipt

```python
from notaryos import verify_receipt

is_valid = verify_receipt(receipt.to_dict())  # True or False, no auth needed
```

## Lookup by Hash

```python
notary = NotaryClient()
result = notary.lookup("e1d66b0bdf3f8a7e...")

if result["found"] and result["verification"]["valid"]:
    print("Receipt is authentic and untampered")
```

## Counterfactual Receipts

Record when your agent chose NOT to act:

```python
receipt = notary.seal("trade.declined", {
    "reason": "risk_threshold_exceeded",
    "action_considered": "trade.execute",
    "decision": "blocked"
})
```

## Receipt Chaining

```python
r1 = notary.seal("file.read", {"file": "report.pdf"})
r2 = notary.seal("summary.generated", {
    "source": "report.pdf",
    "length": 500
}, previous_receipt_hash=r1.receipt_hash)
```

## Error Handling

```python
from notaryos import AuthenticationError, RateLimitError, ValidationError

try:
    receipt = notary.seal("action", {"key": "value"})
except RateLimitError:
    pass  # demo: 10 req/min, upgrade at notaryos.org
except AuthenticationError:
    pass  # invalid key
except ValidationError:
    pass  # bad request
```

## Dependencies

- **`sanitize.py` (included):** Zero external dependencies — uses only Python standard library (`typing`). Pure function, no I/O, no network, no side effects.
- **`notaryos` SDK (installed via pip):** Also uses only the Python standard library — zero third-party dependencies. Source: https://pypi.org/project/notaryos/ | GitHub: https://github.com/hellothere012/notaryos

## Key Points

- `NOTARY_API_KEY` is **optional** — a demo key is auto-injected when not set (10 req/min)
- Set `NOTARY_API_KEY` for production rates (get a key at https://notaryos.org/sign-up)
- Both `sanitize.py` and the `notaryos` SDK use only the Python standard library (zero third-party deps)
- Payloads transmitted via HTTPS to `api.agenttownsquare.com`
- Use `sanitize_payload()` to strip sensitive fields before sealing
- Verification is free and public — no API key needed
- Ed25519 signatures (same scheme as SSH and TLS)

## Links

- Docs: https://notaryos.org/docs
- Privacy: https://notaryos.org/privacy
- Explorer: https://notaryos.org/explore
- API Docs: https://notaryos.org/api-docs
- PyPI: https://pypi.org/project/notaryos/
- npm: https://www.npmjs.com/package/notaryos
- GitHub: https://github.com/hellothere012/notaryos
- License: https://github.com/hellothere012/notaryos/blob/main/LICENSE
