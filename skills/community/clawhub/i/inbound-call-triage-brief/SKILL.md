---
name: inbound-call-triage-brief
displayName: "Inbound Call Triage Brief"
version: "1.0.0"
description: "Triage inbound calls to an AI agent line — classify caller intent, screening questions, escalate-vs-handle rules, message-taking script, and spam signals before the agent picks up."
triggerKeywords:
  - inbound call triage
  - screen incoming call
  - ai receptionist script
  - inbound call routing
  - caller intent classification
  - escalate to human phone
  - inbound call handling
  - answer incoming agent call
  - call screening rubric
  - incoming call playbook
tags:
  - inbound-call
  - incoming-call
  - customer-service
  - receptionist
  - agent-phone-call
license: "MIT"
language: "en"
hasExecutableCode: false
promptOnly: true
execution: "noExec"
---

# Inbound Call Triage Brief

## Purpose

Produce an **inbound triage brief** when a call arrives (or is expected) on an AI agent phone line — PollyReach, Agent Phone Call, OpenPhone, Twilio, etc. Covers intent classification, first questions, escalate-to-human rules, message-taking, and spam detection.

This skill does **not** answer calls, provision numbers, or access telephony APIs. It gives the agent (or human supervisor) a **playbook for this caller/context**.

Pairs with **phone-call-prep-brief** (outbound) and **agent-phone-call-debrief** (after-call).

## When to use

Use when:

- Setting up how an AI line handles **incoming** calls
- A call is ringing and the agent needs a quick routing script
- Defining receptionist / front-desk behavior for an agent number
- User asks to screen, triage, or route inbound callers

## Safety and boundaries

**Do not** collect passwords, OTP codes, full card numbers, or SSNs — even if callers offer them.

**Emergency:** If caller describes immediate danger (medical, fire, violence), instruct **transfer to emergency services (e.g. 911)** — do not attempt AI-only handling.

**Harassment/spam:** Document disengage script; do not engage debate.

**Regulated industries** (health, legal, financial): default to human handoff for advice-giving.

**Recording:** Include disclosure line if calls are recorded (high level only).

## Required inputs

1. **Line purpose** — support, sales, booking, personal screening, mixed.
2. **Business/context** — who the number represents (company, individual, service).
3. **Caller hint** (optional) — known number, CRM name, or “unknown.”
4. **Hours** — 24/7 AI vs business hours with after-hours behavior.
5. **Human backup** — who can take escalations and how (warm transfer, callback).
6. **Must-capture fields** — name, callback number, account ID, etc.

## Workflow

1. Classify expected **caller intents** for this line (≤6 categories).
2. For each intent: handle / message / escalate.
3. Draft **opening script** (≤20 seconds spoken).
4. Define **escalation triggers** (keyword, emotion, VIP, legal threat, etc.).
5. Output triage brief (format below).

## Intent categories (starter set)

Adapt to line purpose; pick 3–6:

| Intent | Typical handle |
|--------|----------------|
| Booking / scheduling | Agent collects slots → confirm |
| Order / account status | Verify identity lightly → lookup or escalate |
| Support issue | Troubleshoot tier-1 → escalate if unresolved |
| Sales inquiry | Qualify → book or escalate |
| Wrong number / spam | Polite disengage |
| VIP / urgent | Fast-track human |

## Output format

### Inbound triage brief — {line or business}

| Field | Value |
|-------|-------|
| Line purpose | … |
| After-hours | … |
| Human backup | … |
| Recording disclosure | yes/no + one-liner |

#### Opening script

What the agent says when answering (friendly, states who they represent, sets expectation).

#### Intent routing table

| Intent | First questions | Agent can resolve? | Escalate when |
|--------|-----------------|--------------------|---------------|
| … | … | yes / partial / no | … |

#### Screening questions (unknown callers)

Numbered list, minimal PII.

#### Message-taking template

If taking a message: fields to capture + read-back script.

#### Spam / robocall signals

Behaviors that trigger short disengage (silent line, obvious pitch, repeated hang-up).

#### Escalation pack

- Trigger list
- Warm handoff line: “I’m connecting you with …”
- If human unavailable: callback promise script

#### Do not do on this line

Bullets (e.g. process payments, give medical advice, promise refunds without policy).

## Quality bar

- **Inbound-first** — opening script assumes caller initiated contact.
- **Escalation is explicit** — not “use judgment.”
- **Short scripts** — speakable in one breath where possible.
- **PII minimal** — collect only must-capture fields.

## Examples

**Good opening:** “Thanks for calling Acme Support — I’m the automated assistant. I can help with order status or scheduling a callback. What are you calling about today?”

**Bad opening:** “Hello, how can I help?” (no context, no boundaries)

**Good escalate trigger:** “Caller requests chargeback over $500 or mentions attorney.”

**Bad escalate trigger:** “If the caller is angry.” (too vague)
