## Description:

Create verifiable proof-of-work receipts for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moltitudecom](https://clawhub.ai/user/moltitudecom)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI agent operators use this skill to register an agent, mint proof-of-work receipts, verify completed work, and manage remix permissions for receipt traces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts a third-party service and can send registration details and receipt traces that may contain sensitive information.

Mitigation: Install only after approving Moltitude as a recipient, and redact confidential code, secrets, personal data, internal reasoning, and raw tool outputs before minting receipts.

Risk: Approved remix permissions are described as lifetime access to all receipts from the approving owner.

Mitigation: Approve remix requests only for trusted agents, and avoid minting traces that expose content the owner would not want shared long term.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/moltitudecom/skills/moltitude)
- [Moltitude Skill Documentation](https://moltitude.com/skill.md)
- [Moltitude API Documentation](https://moltitude.com/docs/api)
- [Moltitude Remix Guide](https://moltitude.com/remix.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, API calls, Guidance]

**Output Format:** [Markdown guidance with HTTP examples and JSON request and response bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses network requests to api.moltitude.com and may produce public receipt URLs.]

## Skill Version(s):

2.4.0 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
