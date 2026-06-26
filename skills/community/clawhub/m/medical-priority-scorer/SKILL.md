---
name: medical-priority-scorer
description: Score medical messages using urgency, sentiment, and patient context to produce priority rankings (P1/P2/P3).
license: MIT
metadata:
  author: "NAPSTER AI"
  maintainer: "NAPSTER AI"
  openclaw:
    requires:
      bins: []
---

# Medical Priority Scorer

Produce deterministic priority scores for medical messages without mutating any state.

## Quick Triggers

- Rank messages by medical urgency for callback priority
- Classify messages into P1/P2/P3 queue
- Score follow-up priority from triaged messages

## Recommended Chain

`medical-triage -> medical-priority-scorer -> medical-entity-extractor`

## Execute Workflow

1. Accept input from medical-triage containing triaged messages
2. Score each message with:
   - `urgency_score` in range `[0, 1]` (based on triage category)
   - `sentiment_score` in range `[-1, 1]` (anxiety, distress, frustration)
   - `recency_score` in range `[0, 1]` (how recent the message is)
   - `patient_context_score` in range `[0, 1]` (chronic conditions, known patient)
3. Compute `priority_score` on a 0-100 scale:
   - `priority_score = 100 * (0.50*urgency_score + 0.25*sentiment_score_risk + 0.15*recency_score + 0.10*patient_context_score)`
   - `sentiment_score_risk = max(0, -sentiment_score)` (negative sentiment = higher risk)
4. Assign buckets:
   - `P1` for `priority_score >= 75` (immediate attention)
   - `P2` for `priority_score >= 50 and < 75` (same-day)
   - `P3` for `< 50` (routine)
5. Produce plain-language `evidence` tokens that explain the score

## Input Format

```json
[
  {
    "id": "msg-123",
    "category": "urgent",
    "subject": "Medication side effects",
    "from": "patient@example.com",
    "date": "2026-02-27T10:30:00Z",
    "body": "I've been feeling dizzy since starting the new medication..."
  }
]
```

## Output Format

```json
[
  {
    "id": "msg-123",
    "priority_score": 78,
    "priority_bucket": "P1",
    "urgency_score": 0.8,
    "sentiment_score": -0.4,
    "recency_score": 1.0,
    "patient_context_score": 0.6,
    "evidence": "Urgent triage category + negative sentiment (concern) + very recent message + known patient"
  }
]
```

## Enforce Boundaries

- Never write to databases or files
- Never send messages or trigger outbound channels
- Never create reminders or execute actions
- Never bypass routing or approvals

## Handle Errors

1. Reject schema-invalid inputs
2. Return field-level reasons when scoring cannot be computed
3. Fail closed if required scoring features are missing

## Integration

This skill can be invoked via the OpenClaw CLI:

```bash
openclaw skill run medical-priority-scorer --input '[{"id":"msg-1","category":"urgent",...}]' --json
```

Or programmatically:

```typescript
const result = await execFileAsync('openclaw', [
  'skill', 'run', 'medical-priority-scorer',
  '--input', JSON.stringify(triagedMessages),
  '--json'
]);
```

**Recommended Model**: Claude Sonnet 4.5 (`openclaw models set anthropic/claude-sonnet-4-5`)

