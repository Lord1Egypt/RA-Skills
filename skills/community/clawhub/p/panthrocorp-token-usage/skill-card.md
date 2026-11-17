## Description:

Multi-agent token burn analysis across all registered OpenClaw agents

This skill is ready for commercial/non-commercial use.

## Publisher:

[panthrocorp](https://clawhub.ai/user/panthrocorp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to analyze token usage and estimated costs across registered OpenClaw agents, grouped by agent and channel category. It helps identify high-spend or high-token categories and keeps a structured usage history for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads token and cost metadata across all registered OpenClaw agents and automatically keeps persistent usage history, which can expose operational patterns to later tools or users with workspace access.

Mitigation: Install only where cross-agent usage analysis and persistent workspace memory are acceptable; review access to token-usage-history.ndjson before sharing the workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/panthrocorp/skills/panthrocorp-token-usage)
- [Project Homepage](https://github.com/PanthroCorp-Limited/openclaw-skills)
- [Release 0.2.2 Comparison](https://github.com/PanthroCorp-Limited/openclaw-skills/compare/token-usage/v0.2.1...token-usage/v0.2.2)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Markdown report with tables and a compact JSON Lines history record]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Always appends one JSON line to token-usage-history.ndjson; optional Markdown logging only when explicitly requested.]

## Skill Version(s):

0.2.2 (source: frontmatter, version.txt, release metadata, CHANGELOG released 2026-04-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
