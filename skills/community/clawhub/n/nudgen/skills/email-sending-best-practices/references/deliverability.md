# Deliverability

## Core Guidance

- Treat deliverability as a system: domain setup, consent quality, sending cadence, and engagement quality all matter.
- Complete SPF, DKIM, and DMARC setup before deep content tuning.
- Warm new sending reputation with expected, high-intent traffic first.
- Expand volume gradually and pause expansion when quality metrics degrade.

## Nudgen-Oriented Sending Context

- Nudgen delivery uses Postmark-backed sending flows.
- Campaign sends should respect suppression and contact status states.
- Open/click/unsubscribe tracking must be operational before large sends.
- Team-scoped settings should be consistent with sender identity and reply handling.

## Warming And Expansion

- Start with onboarding or expected lifecycle sends.
- Expand from recently active recipients to colder cohorts in batches.
- Avoid one-shot large blasts to stale imports on new reputation.

## Signals To Monitor

- delivery success/failure rate
- bounce rate
- unsubscribe rate
- complaint/spam indicators
- click quality and downstream actions

Do not optimize around open rate alone.

## Practical Review Checklist

- domain authentication is complete and verified
- audience quality is reviewed before each major send
- campaign stop/guard rules are configured
- tracking and unsubscribe flows are tested end to end
