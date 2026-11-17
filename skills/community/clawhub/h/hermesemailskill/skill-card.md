## Description:

Hermes Email Skill guides agents through email launch planning, message QA, incident triage, and approval-gated send readiness handoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polnikale](https://clawhub.ai/user/polnikale)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and launch-room participants use this skill to plan, audit, and improve email workflows with concise QA checks, launch status summaries, incident timelines, and approve-or-hold recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email launch recommendations may affect high-impact operational actions such as sends, imports, DNS changes, suppression edits, or production automation changes.

Mitigation: Require explicit approval before live-system actions and keep analysis separate from execution.

Risk: A rushed launch decision may miss audience, personalization, deliverability, compliance, approval, or CTA issues.

Mitigation: Use the operating checklist to verify copy, links, rendering, segment logic, exclusions, sender identity, tracking, monitoring windows, and escalation owners.

## Reference(s):

- [Hermes Email Skill Operating Checklist](references/operating-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with concise tables, timelines, notes, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps live sends, contact imports, DNS changes, suppression edits, and production automation changes behind explicit approval.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
