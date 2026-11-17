## Description:

Use when the user asks how to make money, monetize existing work, grow revenue, choose among projects, find a first customer, improve a cash engine, or invoke MoneyPrinter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bilbop1](https://clawhub.ai/user/bilbop1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Moneyprinter to review recent permitted AI work, identify the nearest credible revenue route, and prepare a bounded payable test. The skill is designed to keep private analysis separate from external actions that require explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests access to recent local AI session history and may encounter sensitive or unrelated work.

Mitigation: Use only explicit, narrowly scoped permission; exclude sensitive sources; avoid credential and environment files; and summarize with sanitized receipts rather than raw session content.

Risk: Revenue recommendations can overstate income, demand, or proof if weak signals are upgraded.

Mitigation: Keep the skill's evidence labels intact and distinguish cash collected, contracted revenue, booked revenue, pipeline signal, estimated value, simulation, and unverified anecdote.

Risk: External outreach, spending, payment collection, publication, or account changes could create unauthorized commitments.

Mitigation: Stage private drafts only until the user gives fresh approval for the exact external action, including channel, audience, message, volume, timing, tool, cost, and risk.

## Reference(s):

- [Evidence standard](references/evidence-standard.md)
- [Route map](references/route-map.md)
- [Safety boundaries](references/safety-boundaries.md)
- [Fourteen-day session scan](references/session-scan.md)
- [Minimal fallback interview](references/interview.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown with structured sections, sanitized receipts, route scoring, experiment briefs, staged drafts, and approval gates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include evidence labels, source-linked summaries, run state, and explicit external-action approval fields.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata.version is 0.1.0-rc.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
