## Description:

Manage BigMailer brands, contacts, and lists through the oo CLI using an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the skill to read and manage BigMailer brands, contacts, and contact lists through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency setup can execute changing remote code and may add agent skills during startup.

Mitigation: Review the CLI and installer deliberately; set OO_SKILLS_SYNC_DISABLED=1 before invoking oo if startup skill synchronization is unwanted.

Risk: BigMailer data passes through OOMOL, and the exact remote installer behavior is unverified.

Mitigation: Confirm OOMOL is suitable for the account's data, inspect installation behavior before use, and retain approval for write and deletion actions.

## Reference(s):

- [BigMailer API documentation](https://docs.bigmailer.io/)
- [BigMailer](https://www.bigmailer.io/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON action payloads and results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs follow the live connector schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
