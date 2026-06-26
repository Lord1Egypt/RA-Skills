name: judgment_event_protocol
description: Cryptographic event logging for autonomous agents. Record tamper-proof judgment, delegation, termination, and verification events using the Judgment Event Protocol. Provides verifiable decision trails with JCS canonicalization and Ed25519 signatures.
user-invocable: true
tags:
  - jep
  - judgment
  - delegation
  - provenance
  - audit
  - accountability
  - jcs
  - ed25519
metadata:
  openclaw:
    requires:
      bins: [python3, pip]
---

# Judgment Event Protocol (JEP)

You have a minimal, verifiable event logging system for AI agent decisions. Use it when you need to record judgments, delegate authority, terminate decision lifecycles, or verify existing events with cryptographic integrity.

## Setup

```bash
pip install jep-protocol
```

## Security Considerations

This skill handles cryptographic keys and external dependencies. Please observe the following practices to ensure safe usage:

- **🔑 Private Key Management**: Private keys should **never** be hardcoded in agent prompts, source files, or shared in conversations. Always store keys using a secure key manager (e.g., environment variables, secret management services, HSMs, or hardware tokens). The code examples below assume `private_key` and `public_key` are securely loaded from such a source.
- **📦 Package Integrity**: The `jep-protocol` PyPI package is open source. Verify its integrity by checking the source code at https://github.com/hjs-spec/jep. Consider pinning the package to a reviewed version hash in your dependency manager.
- **🧪 Environment Isolation**: Before integrating the library into production systems or granting access to sensitive keys, test it in an isolated environment (e.g., a Python virtual environment or a container).

## When to Use This Skill

- When you need to **record an agent's decision** for future audit
- When you **delegate a task** to another agent and need proof of handoff
- When you **terminate a decision process** and want to seal the record
- When you need to **verify the integrity** of an existing event chain
- When building **accountability trails** for compliance or debugging

## Core Verbs

JEP defines four immutable verbs:

| Verb | Name | Purpose |
|:-----|:-----|:--------|
| `J`  | Judge | Initiate a new decision or root audit event |
| `D`  | Delegate | Transfer decision authority to another agent |
| `T`  | Terminate | Close the decision lifecycle |
| `V`  | Verify | Verify authenticity of an existing event |

## Event Structure (JSON Example)

A minimal JEP event before signing:

```json
{
  "jep": "1",
  "verb": "J",
  "who": "did:example:agent-123",
  "when": 1742345678,
  "what": "sha256:e8878aa9a38f4d123456789abcdef01234",
  "nonce": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "aud": "https://platform.example.com",
  "ref": null
}
```

## Core Operations

### Record a Judgment Event (J)

```python
from jep import JEPEvent, Verb

# Assumes private_key is loaded from a secure source
event = JEPEvent(
    verb=Verb.J,
    who="did:example:agent-123",
    what="sha256:hash-of-decision-content",
    aud="https://platform.example.com"
)
receipt = event.sign(private_key)
print(receipt.to_json())
```

### Record a Delegation Event (D)

```python
event = JEPEvent(
    verb=Verb.D,
    who="did:example:agent-123",
    what="sha256:hash-of-delegation-details",
    aud="https://platform.example.com",
    ref="hash-of-parent-event"  # Link to previous event
)
```

### Record a Termination Event (T)

```python
event = JEPEvent(
    verb=Verb.T,
    who="did:example:agent-123",
    what=None,
    aud="https://platform.example.com",
    ref="hash-of-decision-chain-head"
)
```

### Record a Verification Event (V)

```python
event = JEPEvent(
    verb=Verb.V,
    who="did:example:verifier-456",
    what=None,
    aud="https://platform.example.com",
    ref="hash-of-target-event"
)
```

### Verify an Existing Receipt

```python
from jep import verify_receipt

result = verify_receipt(
    receipt_json,
    public_key,
    expected_aud="https://platform.example.com"
)

if result.valid:
    print("Signature valid, chain intact")
else:
    print(f"Verification failed: {result.error}")
    # Possible error codes:
    # - INVALID_SIGNATURE: Signature doesn't match
    # - REPLAY_DETECTED: Nonce already seen
    # - EXPIRED: Timestamp outside allowed window
    # - BROKEN_CHAIN: Parent event hash mismatch
    # - INVALID_AUDIENCE: aud field doesn't match expected value
```

## Optional Privacy Extensions

JEP supports modular extensions for privacy and compliance:

| Extension | Purpose |
|:----------|:--------|
| `digest-only` | Anonymize actor identities with salted hashes |
| `multisig` | Require multiple signatures for distributed accountability |
| `ttl` | Auto-expire events for data retention compliance |
| `storage` | Decouple event storage from protocol for data sovereignty |
| `subject` | Explicitly reference decision subjects for traceability |

## Relationship to HJS and JAC

JEP is the foundational event format for the broader accountability stack:

| Layer | Protocol | Purpose |
|:------|:---------|:--------|
| **Base** | JEP | Tamper-proof event recording (this skill) |
| **Responsibility** | HJS | Human oversight and privacy protection |
| **Causality** | JAC | Cross-agent judgment chain tracking |

JEP events serve as the immutable data layer that HJS and JAC build upon. All three protocols share the same JSON canonicalization (JCS/RFC 8785) and signature scheme (JWS/RFC 7515).

## Links

- **Protocol Documentation**: https://github.com/hjs-spec
- **HJS Foundation**: https://humanjudgment.org
```
