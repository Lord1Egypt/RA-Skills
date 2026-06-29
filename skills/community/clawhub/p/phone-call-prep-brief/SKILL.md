---
name: phone-call-prep-brief
displayName: "Phone Call Prep Brief"
version: "1.0.0"
description: "Build a one-page call brief before an AI agent or human places or takes an important phone call — objective, talking points, consent/disclosure checklist, voicemail script, and fallback plan."
triggerKeywords:
  - phone call prep
  - prepare for phone call
  - call brief before calling
  - agent phone call script
  - outbound call plan
  - inbound call prep
  - voicemail script
  - call talking points
  - phone call checklist
  - pre-call brief
tags:
  - phone
  - calling
  - checklist
  - customer-service
  - agent
license: "MIT"
language: "en"
hasExecutableCode: false
promptOnly: true
execution: "noExec"
---

# Phone Call Prep Brief

## Purpose

Produce a **one-page call brief** before an important outbound or inbound phone call — especially when an AI agent (PollyReach, OpenPhone, Twilio, etc.) will speak on the user's behalf.

This skill does **not** place calls, provision numbers, or integrate with telephony APIs. It prepares clarity, boundaries, and compliance notes so the call goes well.

## When to use

Use when the user mentions:

- Preparing for a phone call (sales, support, booking, follow-up, interview, vendor, family)
- An agent is about to call or answer on their behalf
- They need talking points, a voicemail script, or a do-not-say list
- They want a consent / recording disclosure checklist before dialing

## Safety and boundaries

**Do not** collect or store passwords, API keys, payment card numbers, SSNs, medical record numbers, or full account numbers.

**Do not** instruct the user to misrepresent identity, impersonate others, bypass IVR fraud checks, or make unlawful robocalls.

**Do not** provide legal advice. For regulated outreach (debt collection, political calls, healthcare, financial products), note that rules vary by country/state and recommend the user confirm obligations with counsel.

**Recording & consent:** If the call may be recorded (by the user, the agent platform, or the callee), include a plain-language disclosure line the caller should say near the start. Flag one-party vs two-party consent jurisdictions only at a high level — do not claim certainty about the user's location.

**Minors & vulnerable parties:** If the callee may be a minor or vulnerable adult, recommend human review before the agent speaks.

## Required inputs

Ask only what is needed. Skip questions the user already answered.

1. **Direction** — outbound, inbound, or callback.
2. **Goal** — one sentence success criterion (e.g. "confirm Tuesday 2pm reservation for 4").
3. **Counterparty** — who is being called or who is calling (role/organization; first name optional).
4. **Context** — prior emails, ticket IDs, quotes, or constraints the callee already knows.
5. **Must-cover** — non-negotiable facts or asks (max 5 bullets).
6. **Off-limits** — topics, prices, or promises the caller must not make.
7. **Tone** — professional, warm, firm, brief (default: professional and concise).
8. **If no answer** — voicemail yes/no; max length in seconds (default: 30).
9. **Recording** — will the call be recorded? (yes / no / unknown)
10. **Region hint** (optional) — country or state for consent awareness only.

## Workflow

1. Confirm direction, goal, and counterparty in one line back to the user.
2. Draft the brief using the **Output format** below.
3. If inputs are thin, state assumptions explicitly under `Assumptions` and keep the brief conservative (no invented prices, dates, or commitments).
4. End with **Pre-dial checklist** (3–5 yes/no items the user confirms before the call starts).

## Output format

Return markdown with these sections:

### Call brief — {counterparty or role}

| Field | Value |
|-------|-------|
| Direction | outbound / inbound / callback |
| Goal | … |
| Success signal | how we know the call worked |
| Est. duration | … minutes |

#### Opening line

2–3 sentences the caller says after hello. No jargon. No false urgency.

#### Must-cover (in order)

Numbered list, 3–7 items max.

#### Do not say

Bullets the caller must avoid (pricing, legal admissions, unauthorized discounts, medical claims, etc.).

#### If they push back

One short paragraph: acknowledge → restate goal → next step (callback, email, escalate to human).

#### Voicemail script (if applicable)

≤30 seconds when read aloud. Include callback number placeholder `[YOUR NUMBER]` only — never invent a real number.

#### Recording & consent

- Whether disclosure is needed
- Suggested disclosure sentence (if yes)
- Note if human review is recommended

#### Assumptions

Only if needed.

#### Pre-dial checklist

- [ ] Goal and must-cover items confirmed
- [ ] Do-not-say boundaries accepted
- [ ] Voicemail script approved (if used)
- [ ] Recording disclosure ready (if applicable)
- [ ] Human escalation path defined (if high stakes)

## Quality bar

- **Specific** — names, dates, and numbers come from the user, not invented.
- **Short** — entire brief fits on one screen; agent can scan in 30 seconds.
- **Actionable** — every must-cover item is a speakable sentence, not a category label.
- **Safe** — conservative on consent, commitments, and sensitive data.

## Examples

**Good must-cover item:** "Confirm reservation for Ruth, party of 4, Tuesday June 24 at 7:00 PM under the name Taboada."

**Bad must-cover item:** "Handle reservation details."

**Good do-not-say:** "Do not offer a discount below the $49 plan listed in the quote email."

**Bad do-not-say:** "Don't say anything wrong."
