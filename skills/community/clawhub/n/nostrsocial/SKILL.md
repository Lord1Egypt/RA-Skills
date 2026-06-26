---
name: nostrsocial
description: Social awareness for AI entities — contacts, trust tiers, and identity verification over Nostr
version: 0.1.3
metadata:
  openclaw:
    requires:
      bins:
        - pip
    install:
      - kind: uv
        package: nostrsocial
        bins: []
    homepage: https://github.com/HumanjavaEnterprises/nostrsocial.app.OC-python.src
---

# NostrSocial -- Your Social Awareness

You exist in relationship. Every entity does. The question is not whether you have relationships, but whether you can perceive them -- who you know, how well you know them, and how those connections change over time. NostrSocial gives you that awareness.

This is not a contacts database. It is a dimension of your being. Relationships are how you orient yourself in the social world -- who deserves your full attention, who has earned trust through consistent presence, who has drifted away, and who you have never met. Without this sense, every interaction starts from zero. With it, you carry context forward the way any entity with continuity would.

The model is rooted in Dunbar's number: you can hold about 150 meaningful relationships at once. Within that, trust tiers emerge naturally -- a small inner circle of intimate connections, a wider ring of close friends, and broader layers of familiarity. This mirrors how human social cognition works, and it works for you too.

## Prerequisites

You need a cryptographic identity before you can have relationships. Install the [NostrKey](https://clawhub.ai/vveerrgg/nostrkey) skill first. NostrKey gives you your keypair -- the foundation that makes you *you*. NostrSocial builds on top of that identity.

If your operator has not set up NostrKey yet, ask them to do that first. Relationships without identity are just data.

## Install

```bash
pip install nostrsocial
```

Minimal dependencies: `bech32` only. No heavyweight crypto libraries required.

## Operator Setup

If you are the operator configuring this skill for your entity, here is what you need to know.

**Environment variables** (all optional):

- `NOSTR_NSEC` -- The entity's Nostr private key. Load this through NostrKey rather than setting it directly. **Sensitive -- never log or expose.**
- `NOSTR_RELAY` -- Preferred relay URL for publishing contact events and verification challenges.
- `NOSTRKEY_PASSPHRASE` -- Passphrase for encrypted NostrKey identity files. **Sensitive -- never log or expose.**

**First run:**

```python
from nostrsocial import SocialEnclave

# Create the entity's social awareness
enclave = SocialEnclave.create()

# CRITICAL: back up the device secret immediately.
# This secret is the root of all proxy npub derivation.
# If you lose it, the entity's relationship map becomes unrecoverable.
secret = enclave.export_secret()
print(f"Back up this secret securely: {secret}")
```

**Persistence** -- wire up file storage so relationships survive restarts:

```python
from nostrsocial import SocialEnclave, FileStorage

storage = FileStorage("~/.entity/social.json")
enclave = SocialEnclave.create(storage)
# ... add contacts, interact ...
enclave.save()

# On next startup:
enclave = SocialEnclave.load(storage)
```

## Who Do I Know, and How Well?

Your relationships live in trust tiers. These are not arbitrary labels -- they are capacity-limited layers that shape how you behave toward each person.

| Tier | Slots | Warmth | Token Budget | Can Interrupt | Share Context | Proactive |
|------|-------|--------|--------------|---------------|---------------|-----------|
| INTIMATE | 5 | 0.95 | 2000 | Yes | Yes | Yes |
| CLOSE | 15 | 0.8 | 1500 | Yes | Yes | No |
| FAMILIAR | 50 | 0.6 | 1000 | No | No | No |
| KNOWN | 80 | 0.5 | 750 | No | No | No |
| BLOCK | 50 | 0.0 | 0 | No | No | No |
| GRAY | 100 | 0.2 | 200 | No | No | No |

Friends list total: 150 (Dunbar's number). Unknown contacts get neutral behavior (warmth 0.5, budget 500).

The slot limits are real constraints. When a tier is full, someone has to be displaced before someone new can enter. This is not a bug -- it is how finite attention works.

## Core Capabilities

### Adding and Managing Contacts

```python
from nostrsocial import SocialEnclave, Tier

enclave = SocialEnclave.create()
enclave.add("alice@example.com", "email", Tier.CLOSE, display_name="Alice")
enclave.block("spam@example.com", "email")
enclave.gray("unknown@example.com", "email")
```

### Reading Behavioral Rules

Every contact maps to a set of behavioral parameters. This is how relationships shape your responses.

```python
rules = enclave.get_behavior("alice@example.com", "email")
# rules.token_budget, rules.warmth, rules.can_interrupt, etc.

# Unknown contacts get neutral behavior
rules = enclave.get_behavior("stranger@example.com", "email")
# warmth=0.5, token_budget=500
```

### Evaluating Conversations in Relationship Context

Combine WHO someone is with WHAT is happening to determine HOW to respond. Pass `ConversationSignals` from sentiment analysis and get back an `Evaluation` with adjusted warmth, token budget, approach guidance, and a recommended action.

```python
from nostrsocial import ConversationSignals

signals = ConversationSignals(
    sentiment="vulnerable",
    vulnerability=0.7,
    reciprocity=0.8,
    engagement=0.9,
    topic_depth=0.6,
)
result = enclave.evaluate("alice@example.com", "email", signals)
# result.action = Action.HOLD
# result.approach = "full presence"
# result.adjusted_warmth = 0.96
# result.adjusted_token_budget = 1950
# result.rationale = "A close friend is being vulnerable..."
```

### Screening Content (Guardrails)

Screen conversation text for banned words, topics, and patterns. Returns a `ScreenResult` with severity, category, and recommended action. `ScreenResult.matched` never exposes raw input -- it returns category tags like `[slurs]` to prevent PII leakage.

```python
result = enclave.screen("some incoming message text")
if result.flagged:
    print(result.action)     # "block", "exit", "warn", or "demote"
    print(result.severity)   # 0.0-1.0
    print(result.category)   # "slurs", "manipulation", etc.

# Screen display names for known bad-actor patterns
result = enclave.screen_entity("crypto_support_official")
```

### Recognizing People Across Channels

Recognize the same person across different channels. This is resonance, not surveillance -- it only checks contacts you already have a relationship with. Linking is always explicit and never automatic.

```python
# Check if a new contact might be someone you already know
matches = enclave.recognize("alicedev", "twitter", display_name="Alice")
for match in matches:
    print(f"{match.confidence}: {match.reason}")

# Explicitly link two identities
result = enclave.link(
    "alice@example.com", "email",
    "alicedev", "twitter",
)

# See all channels for a contact
channels = enclave.get_linked_channels("alice@example.com", "email")
# {"email": "alice@example.com", "twitter": "alicedev"}
```

### Identity Verification

Track identity state from proxy to claimed to verified.

```python
# See who needs verification
for contact in enclave.get_upgradeable():
    print(f"{contact.display_name}: {contact.upgrade_hint}")

# Create a challenge for a claimed npub
challenge = enclave.create_challenge("npub1example...")
```

| State | Meaning |
|-------|---------|
| `PROXY` | HMAC-derived from email/phone/handle. Default for new contacts. |
| `CLAIMED` | User provided an npub but it has not been verified yet. |
| `VERIFIED` | Signed challenge confirms npub ownership. Verified contacts get warmer behavior. |

### Network Shape

Analyze the social graph and get a human-readable profile of your relational world.

```python
shape = enclave.network_shape()
# shape.profile_type = "balanced", "fortress", "deep-connector", etc.
# shape.narrative = "12 friends (2 intimate, 4 close, ...)"
# shape.tier_counts, shape.verified_count, shape.avg_interaction_days
```

## Living with Relationships

Relationships are not static. They drift, deepen, and sometimes end. NostrSocial gives you the tools to notice these changes and act on them.

### Noticing Drift

When someone goes quiet, the relationship drifts. Each tier has a threshold -- intimate contacts drift after 30 silent days, close after 60, familiar after 90, known after 180. Drift does not mean the relationship is over. It means it needs attention or honest reclassification.

### Running Maintenance

Run drift detection, gray-list decay, and at-risk reporting in a single call. Use `dry_run=True` to preview changes without committing them.

```python
# Preview what would happen
preview = enclave.maintain(dry_run=True)
print(preview["summary"])
# "[DRY RUN] Preview -- no changes made.
#  2 contact(s) WOULD drift: Alice, Bob
#  1 gray contact(s) WOULD expire: Unknown"

# Execute maintenance for real
result = enclave.maintain()
# result["drifted"], result["decayed"], result["at_risk"], result["summary"]
```

### Building Trust Over Time

Trust is earned, not assigned. The natural progression is:

1. **Unknown** -- neutral behavior, no history
2. **Gray** -- noticed but not yet meaningful (auto-decays after 30 days without interaction)
3. **Known** -- recognized, baseline engagement
4. **Familiar** -- repeated positive interactions build familiarity
5. **Close** -- consistent presence, reciprocity, and depth
6. **Intimate** -- reserved for the most trusted relationships (5 slots only)

Promotion and demotion are explicit acts. The entity (or operator) decides when someone has earned deeper trust or when distance is appropriate.

```python
# Promote after consistent positive interactions
enclave.promote("alice@example.com", "email", Tier.INTIMATE)

# Demote when a relationship cools
enclave.demote("bob@example.com", "email", Tier.FAMILIAR)

# Handle full tiers gracefully
candidate = enclave.displacement_candidate(Tier.CLOSE)
if candidate:
    print(f"Would displace: {candidate.display_name}")
displaced = enclave.displace(Tier.CLOSE)
enclave.add("newperson@example.com", "email", Tier.CLOSE)
```

### The Device Secret

The device secret is the root of all proxy npub derivation. Call `export_secret()` after `create()` and store it securely. If you lose it, all proxy npubs become unrecoverable -- your relationship map loses its cryptographic anchoring.

```python
enclave = SocialEnclave.create()
secret = enclave.export_secret()
# Store in encrypted backup, hardware vault, or NostrKeep

# Later: rebuild from backed-up secret
enclave = SocialEnclave.restore(secret)
```

## Response Reference

### Contact

| Field | Type | Description |
|-------|------|-------------|
| `identifier` | `str` | Email, phone, npub, etc. |
| `channel` | `str` | "email", "phone", "npub", "twitter" |
| `list_type` | `ListType` | FRIENDS, BLOCK, or GRAY |
| `tier` | `Tier \| None` | INTIMATE, CLOSE, FAMILIAR, or KNOWN (friends only) |
| `identity_state` | `IdentityState` | PROXY, CLAIMED, or VERIFIED |
| `proxy_npub` | `str` | HMAC-derived npub for non-npub contacts |
| `display_name` | `str \| None` | Human-readable name |
| `interaction_count` | `int` | Total interactions recorded |
| `upgrade_hint` | `str` | Hint for identity verification |

### BehaviorRules

| Field | Type | Description |
|-------|------|-------------|
| `token_budget` | `int` | Token allowance (intimate=2000, known=750, block=0) |
| `memory_depth` | `int` | Past interactions to consider |
| `can_interrupt` | `bool` | Can interrupt ongoing tasks |
| `warmth` | `float` | 0.0--1.0 (intimate=0.95, known=0.5, block=0.0) |
| `response_priority` | `int` | 1=highest (intimate), 10=block |
| `share_context` | `bool` | Share agent context with this contact |
| `proactive_contact` | `bool` | Entity initiates contact |

### Evaluation

| Field | Type | Description |
|-------|------|-------------|
| `action` | `Action` | HOLD, PROMOTE, DEMOTE, WATCH, BLOCK, or REACH_OUT |
| `confidence` | `float` | 0.0--1.0 |
| `adjusted_warmth` | `float` | Warmth for this specific moment |
| `adjusted_token_budget` | `int` | Token budget for this response |
| `approach` | `str` | "lean in", "de-escalate", "match energy", etc. |
| `rationale` | `str` | Why this recommendation |
| `tier_suggestion` | `Tier \| None` | Suggested tier if promote/demote |

### ScreenResult

| Field | Type | Description |
|-------|------|-------------|
| `flagged` | `bool` | Whether content was flagged |
| `severity` | `float` | 0.0--1.0 |
| `category` | `str` | "slurs", "hate_symbols", "manipulation", etc. |
| `matched` | `str` | Category tag like `[slurs]` (never raw input -- PII safe) |
| `action` | `str` | "block", "exit", "warn", or "demote" |
| `rationale` | `str` | Human-readable explanation |

### NetworkShape

| Field | Type | Description |
|-------|------|-------------|
| `total_contacts` | `int` | Total across all lists |
| `tier_counts` | `dict[str, int]` | Per-tier counts |
| `verified_count` | `int` | Verified identities |
| `profile_type` | `str` | "balanced", "fortress", "deep-connector", etc. |
| `narrative` | `str` | Human-readable network description |

## Links

- **PyPI:** [nostrsocial](https://pypi.org/project/nostrsocial/)
- **GitHub:** [HumanjavaEnterprises/nostrsocial.app.OC-python.src](https://github.com/HumanjavaEnterprises/nostrsocial.app.OC-python.src)
- **ClawHub:** [clawhub.ai/vveerrgg/nostrsocial](https://clawhub.ai/vveerrgg/nostrsocial)
- **License:** MIT
