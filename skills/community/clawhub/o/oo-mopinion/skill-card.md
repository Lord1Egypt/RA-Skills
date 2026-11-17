## Description:

Search and read feedback, datasets, reports, deployments, fields, and account details in Mopinion through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and analysts use this skill to inspect Mopinion account, dataset, report, deployment, field, and feedback data through an existing OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI installation and insufficiently disclosed changes to agent skills need review.

Mitigation: Review and explicitly approve CLI installation before enabling automatic setup. Prefer a verified release, and consider disabling bundled-skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: The remote installer payloads and hosted service implementation were not verified, and OOMOL mediates access to connected Mopinion data.

Mitigation: Review the installer and service trust before setup, and use the documented read actions only for the intended connected account.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Mopinion API documentation](https://developer.mopinion.com/api/)
- [Mopinion](https://www.mopinion.com)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text, JSON]

**Output Format:** [Natural-language responses and JSON data returned by the Mopinion connector]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented account and feedback information]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
