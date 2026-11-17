## Description:

Use MSX when a user asks to scout market opportunities, decide what to build, identify a market gap, find recent demand signals, or run MSX market intelligence through an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tornikeo](https://clawhub.ai/user/tornikeo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and founders use MSX to scout buildable market opportunities, identify market gaps, and find recent demand signals through the MSX service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates authority to a hosted skill file that can change after review.

Mitigation: Use only if the user trusts msx.dev to control future agent instructions, and review the hosted instructions before executing MSX workflows.

Risk: MSX workflows may involve confidential product ideas, market strategy, authentication, billing, or sensitive queries.

Mitigation: Require explicit user confirmation before authentication, billing, or sending sensitive market-research queries to the MSX service.

## Reference(s):

- [MSX homepage](https://msx.dev)
- [MSX hosted skill contract](https://msx.dev/skill.md)
- [MSX API base](https://api.msx.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with API-derived findings, citations, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated MSX API calls, polling status, market-opportunity findings, confidence, urgency, risk notes, and next actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
