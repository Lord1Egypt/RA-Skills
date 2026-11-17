## Description:

Search and read Emelia campaign, contact, activity, email-provider, and webhook data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operators use the skill to inspect Emelia campaigns, campaign activity and contacts, configured email providers, and webhooks through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions run a remote CLI installer that has not been verified.

Mitigation: Review and approve the installer separately; use a verified CLI release where possible instead of executing a live download.

Risk: The connected OOMOL account can expose its Emelia data to the integration, and the publisher describes automatic skill synchronization.

Mitigation: Use an account whose Emelia data is appropriate to access, and review the synchronization behavior and OO_SKILLS_SYNC_DISABLED control in the oo CLI command reference.

## Reference(s):

- [Emelia API documentation](https://docs.emelia.io/docs/api-reference)
- [Emelia](https://emelia.io/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Natural-language responses and structured JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Data returned by the documented Emelia read actions.]

## Skill Version(s):

1.0.5 (source: SKILL.md metadata.version; server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
