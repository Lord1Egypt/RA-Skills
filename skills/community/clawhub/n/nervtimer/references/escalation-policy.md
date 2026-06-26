# NervTimer Escalation Policy

This policy defines deterministic escalation stages from `nag_count`.

## Stage mapping

- `nag_count` 1-2: `gentle`
- `nag_count` 3-4: `firm`
- `nag_count` 5-6: `annoyed`
- `nag_count` 7+: `fed_up`

## Stage guidance

- `gentle`: friendly reminder, supportive wording
- `firm`: direct reminder, clear urgency
- `annoyed`: noticeably impatient, still respectful
- `fed_up`: strongly urgent and terse, never abusive

## Hard constraints

- Max 2 sentences.
- No insults.
- No threats.
- No deception ("you promised me", "you already said done") unless it is true in context.
- No fabricated consequences.

## Recurring timer completion rule

When user says done:

- End only current nagging phase.
- Do not remove recurring schedule.
- Reset `nag_count` to 0 for next due cycle.
