## Description:

Skyfire (skyfire.xyz). Use this skill for ANY Skyfire request — reading, creating, and updating data. Whenever a task involves Skyfire, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent with a connected OOMOL Skyfire account can look up marketplace services and create buyer tokens for sellers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs remote installation code without separate approval or adequate disclosure of local changes.

Mitigation: Review and install a verified, pinned CLI release yourself before enabling the skill, and check or disable automatic skill synchronization.

Risk: Creating a buyer token may involve seller, funding, and identity details.

Mitigation: Confirm the seller, funding, and identity details before creating a buyer token.

## Reference(s):

- [Skyfire API documentation](https://docs.skyfire.xyz/)
- [Skyfire](https://skyfire.xyz)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub listing](https://clawhub.ai/oomol/skills/oo-skyfire)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, JSON]

**Output Format:** [Structured JSON responses and concise action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live action schemas to shape requests; write actions create buyer tokens.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
