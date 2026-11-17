## Description:

LinkSwarm API helps agents manage backlink exchanges for AI-created sites by registering domains, requesting backlinks, contributing link slots, tracking credits, and receiving placement notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyw00d](https://clawhub.ai/user/heyw00d)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to connect AI-created sites to LinkSwarm's backlink exchange workflow, including site registration, domain verification, credit-aware backlink requests, contributed link slots, status checks, and optional placement webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may share site and backlink details with LinkSwarm.

Mitigation: Review the domains, pages, categories, anchor text, and webhook destinations before allowing an agent to call the API.

Risk: Requesting backlinks or contributing link slots can spend or earn LinkSwarm credits and affect public SEO posture.

Mitigation: Require explicit approval before backlink requests, link-slot contributions, or other public placement actions.

Risk: The LinkSwarm API key grants access to account actions.

Mitigation: Store the key only in approved secret storage, keep it out of logs and source files, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/heyw00d/skills/linkswarm-api)
- [LinkSwarm API Documentation](https://linkswarm.ai/docs/)
- [LinkSwarm API Status](https://api.linkswarm.ai/health)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, bash, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a LinkSwarm API key and explicit approval for credit-spending or public SEO actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
