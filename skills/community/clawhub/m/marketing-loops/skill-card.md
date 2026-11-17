## Description:

Helps agents design, adapt, and schedule recurring marketing workflows with explicit cadence, state, self-checks, stop conditions, and human checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coreyhaines31](https://clawhub.ai/user/coreyhaines31)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, founders, and agents use this skill to turn recurring marketing checks into repeatable loops for SEO, paid acquisition, activation, retention, revenue, referrals, and marketing operations. It is intended to plan loop bodies, schedule cadence, stage outputs, and define approval points rather than autonomously spend, publish, or contact customers by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A scheduled marketing loop could spend money, send messages, publish content, or modify live systems without sufficient review.

Mitigation: Use explicit caps, allowlists, review queues, compliance checks, and a documented kill switch before allowing any live action.

Risk: Loops that retain raw personal data in state or logs could increase privacy and compliance exposure.

Mitigation: Store only the minimum needed state, use internal IDs or hashes instead of raw PII, and respect suppression, consent, opt-out, and deletion requirements.

Risk: Loops can act repeatedly on noisy, stale, or broken data and create busywork or harmful duplicate actions.

Mitigation: Require self-checks, durable idempotency state, cooldowns, run logs, stop conditions, and human escalation for data outages or high-impact anomalies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/coreyhaines31/skills/marketing-loops)
- [Marketing Loop Catalog](references/loop-catalog.md)
- [Loop Guardrails & Compliance](references/loop-guardrails.md)
- [Loop Orchestration & Rollout](references/loop-orchestration.md)
- [Loop State & Run Logging](references/loop-state.md)
- [Loop Template](references/loop-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with loop specifications, staged drafts, reports, schedule examples, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce state-file suggestions, run-log formats, cron examples, and review checkpoints for scheduled marketing loops.]

## Skill Version(s):

1.2.0 (source: skill frontmatter and parsed metadata); release package version 1.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
