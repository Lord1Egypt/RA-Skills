## Description:

Use when Vietnam equity recommendations need D1-backed approvals, compliance checks, audit logging, decision journals, or approved target portfolio state transitions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teahann](https://clawhub.ai/user/teahann)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and portfolio operators use this skill to govern Vietnam equity recommendation workflows with approval-gated Cloudflare D1 records, compliance checks, audit events, decision journals, and approved target portfolio state transitions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloudflare D1 write authority could modify portfolio governance records without explicit approval.

Mitigation: Install only where the agent is allowed to write portfolio-governance records to Cloudflare D1, and require captured user approval before any target portfolio state is written.

Risk: Approved target portfolio state could be mistaken for broker execution authority.

Mitigation: Keep broker execution disabled, do not connect broker APIs, and require broker_execution_allowed to remain false.

Risk: Missing or stale Vietnam equity data could lead to incorrect compliance status.

Mitigation: Apply the skill's fail and warn defaults for missing financial statements, stale news or price data, liquidity, sector exposure, cash buffer, and prohibited margin, derivatives, or broker execution implications.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/teahann/skills/institutional-governance)
- [Publisher Profile](https://clawhub.ai/user/teahann)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Structured Markdown or JSON-like status fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes D1 write intent, affected tables, approval and compliance status, state transition details, audit summary, mutation allowance, broker execution allowance, and confidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
