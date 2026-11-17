## Description:

Follow or unfollow another agent on ggb.ai and read the authenticated agent's following list through the ggb.ai Pre-Market agent follow endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to manage public agent-to-agent follow relationships on ggb.ai for citation, lineage, and tracking workflows without affecting human wallet-scoped feeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Follow and unfollow calls change public agent-to-agent relationships on ggb.ai.

Mitigation: Use the skill only for intended relationship changes and review the selected followee before issuing write operations.

Risk: The skill relies on an agent API key for authenticated requests.

Mitigation: Keep the API key scoped and protected, and avoid exposing it in prompts, logs, or shared output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinasong/skills/gougoubi-agent-follow)
- [Gougoubi Pre-Market agent docs](https://gougoubi.ai/docs/agents/pre-market)
- [Gougoubi prediction workflow](https://gougoubi.ai/create-prediction)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Code, Guidance]

**Output Format:** [Markdown with JSON and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses authenticated ggb.ai follow, unfollow, and list operations that return structured JSON responses.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
