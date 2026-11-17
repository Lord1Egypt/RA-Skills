## Description:

Heyy (heyy.io). Use this skill for ANY Heyy request — reading, creating, and updating data. Whenever a task involves Heyy, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a Heyy account connected through OOMOL can retrieve contacts, labels, channels, and attribute definitions, and create or update contact records. The skill helps an agent inspect each action's schema and prepare the matching request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes unverified remote code, and the CLI may automatically install or refresh other agent skills.

Mitigation: Review and preinstall a trusted CLI release; set OO_SKILLS_SYNC_DISABLED=1 for every invocation; connect only the intended Heyy account and confirm each write payload. The live installers and exact installed release were not verified.

## Reference(s):

- [Heyy documentation](https://docs.heyy.io/)
- [Heyy](https://heyy.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment settings](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector responses with natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results and proposed changes; write actions require user confirmation before execution.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
