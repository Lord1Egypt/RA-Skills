## Description:

Government contract and federal award data for AI agents to find US federal awards by company or keyword, identify recent winners, and surface GovCon sales-intent signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colinhughes2121](https://clawhub.ai/user/colinhughes2121)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and business development or research users use this skill to look up US federal contract awards by company or keyword, find recent winners, and qualify B2G leads or competitors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API calls may trigger USDC wallet payments without clear per-call confirmation or spend limits.

Mitigation: Review wallet controls before installing, require per-call confirmation where available, and set spend limits before use.

Risk: Queries may disclose confidential client names, internal strategy keywords, or sensitive lead lists to the provider.

Mitigation: Avoid sensitive queries unless the data is approved for sharing with the provider.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colinhughes2121/skills/government-contracts-federal-awards)
- [GoCreative API](https://api.gocreativeai.com)

## Skill Output:

**Output Type(s):** [API Calls, Guidance]

**Output Format:** [JSON responses from HTTPS GET endpoints with concise agent-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid per call in USDC via x402; listed endpoints are approximately $0.05 per call.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
