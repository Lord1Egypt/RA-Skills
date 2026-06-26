# Pipeline Signals

Use this file when the task needs scoring logic, dwell-time heuristics, or stage-risk reasoning.

## Minimum Scoring Model

A practical priority model can combine four dimensions:
- impact: deal size, strategic value, or expansion value
- urgency: overdue next step, close date pressure, procurement deadline
- momentum: recent reply, meeting booked, stage progression, clear champion
- risk: silence, no next step, repeated objection loops, stage stagnation

Simple rule:
- high impact + high urgency + still controllable = today priority
- high impact + low signal + long stagnation = manager attention, not always top outreach priority

## Derived Field Heuristics

Useful derived fields:
- `days_since_last_touch`
- `days_in_stage`
- `days_overdue_next_step`
- `reply_gap_days`
- `close_date_slip_count`
- `has_named_decision_process`
- `has_next_meeting`
- `champion_strength`

If the source does not provide these directly, infer them from available timestamps and notes.

## Stage Dwell Guidelines

These are default heuristics, not laws. Adjust if the user's motion is enterprise, SMB, agency, or founder-led.

### New Lead / First Contact
- healthy: 1 to 3 business days
- warning: 4 to 7 business days with no real touch
- action: send the first concrete ask, not a generic hello

### Discovery
- healthy: 5 to 10 business days
- warning: discovery completed but no next meeting, no problem statement, or no buyer map
- action: confirm pain, stakeholders, and next milestone

### Demo / Trial
- healthy: 7 to 14 business days
- warning: demo happened but no usage, no evaluation plan, or no technical owner
- action: anchor on success criteria and decision path

### Proposal / Quote
- healthy: 5 to 10 business days
- warning: proposal sent with no response, no review date, or no decision process
- action: ask for review call or explicit decision timing

### Procurement / Security / Legal
- healthy: 10 to 20 business days
- warning: labeled as "legal" or "procurement" but no owner, no ticket, no target date
- action: identify blocker owner and unblock sequence

### Verbal Commit / Close Plan
- healthy: 3 to 7 business days
- warning: verbal yes but no paper process, no signature path, or no implementation handoff
- action: convert intent into dated commitments

## Risk Signals

Strong risk signals:
- customer stopped replying after a proposal or pricing discussion
- close date moved more than once without a clear reason
- the deal has no next step owner
- multiple internal notes exist but no external progress
- champion left, changed role, or lost urgency
- repeated requests for materials without decision movement
- competitor appears late and urgency drops
- discount requests appear before value is accepted

Moderate risk signals:
- long gaps between touches
- stage name looks advanced but notes are still early
- all activity is seller-side follow-up
- next step exists but is vague

## Ranking Guidance For "Top 5 Today"

Promote deals when:
- there is a believable path to movement today
- a message, call, or escalation can change the outcome
- the next action is obvious

Demote deals when:
- no one knows the buying process
- the account is not responding and there is no new angle
- the stage is inflated
- the only reason it ranks high is amount

## Disqualify Or Recycle Guidance

Recommend recycle or disqualification when:
- there is no active pain and no timeline
- follow-up has become repetitive with no new information
- the opportunity lives in pipeline for optics only
- the buyer repeatedly misses agreed next steps with no recovery signal

Say this directly. Healthy pipeline hygiene is part of revenue discipline.
