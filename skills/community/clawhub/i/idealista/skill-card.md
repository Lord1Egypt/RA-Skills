## Description:

Query Idealista API via idealista-cli (OAuth2 client credentials).

This skill is ready for commercial/non-commercial use.

## Publisher:

[quifago](https://clawhub.ai/user/quifago)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to configure Idealista API credentials, run idealista-cli commands, search real estate listings, and compute listing statistics from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a third-party idealista-cli repository.

Mitigation: Confirm the repository is acceptable for the deployment environment before installation.

Risk: Idealista API client credentials may be stored locally if persistent CLI configuration is used.

Mitigation: Prefer temporary environment variables and protect IDEALISTA_API_SECRET like any other API credential.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/quifago/skills/idealista)
- [idealista-cli GitHub Repository](https://github.com/quifago/idealista-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks and natural-language examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and Idealista OAuth2 client credentials supplied through IDEALISTA_API_KEY and IDEALISTA_API_SECRET.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
