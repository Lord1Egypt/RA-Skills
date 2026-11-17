## Description:

Provides fintech company and bank financial analysis using SEC filings, CFPB complaints, FDIC data, market snapshots, and related financial data sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to connect an agent to Pipeworx-hosted fintech research tools for company deep dives, bank health checks, market snapshots, and granular public-data lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes financial research through a third-party gateway.

Mitigation: Use it only with information suitable for Pipeworx processing and avoid confidential plans, customer data, personal complaint details, or sensitive investment interests unless provider controls are documented.

Risk: The artifact recommends remember/recall for intermediate findings without documenting storage scope, retention, deletion, or isolation controls.

Mitigation: Avoid saving intermediate findings until Pipeworx documents storage, retention, deletion, and isolation behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brucegutman/skills/pipeworx-fintech-analyst)
- [Pipeworx Fintech Intel MCP Gateway](https://gateway.pipeworx.io/mcp?task=fintech%20analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON configuration snippets and agent-facing analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include financial summaries, public-data lookups, market snapshots, and intermediate findings saved through provider tools.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
