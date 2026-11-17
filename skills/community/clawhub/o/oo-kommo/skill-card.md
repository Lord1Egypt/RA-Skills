## Description:

Retrieves account, company, contact, lead, pipeline, task, and user data from a connected Kommo account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and operations teams use this skill to look up records and account details in a connected Kommo CRM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup can run a downloaded CLI installer whose contents were not verified.

Mitigation: Review and explicitly authorize installation before running it; prefer a verified, fixed release.

Risk: The CLI may automatically synchronize additional persistent agent skills.

Mitigation: Decide whether to allow synchronization; set OO_SKILLS_SYNC_DISABLED to opt out.

Risk: Connecting Kommo gives OOMOL access to CRM data, while the connector implementation was not verified.

Mitigation: Connect only an account whose data OOMOL is authorized to access, and review the requested connection scopes.

## Reference(s):

- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Kommo website](https://www.kommo.com/)
- [Kommo API documentation](https://developers.kommo.com/docs/long-lived-token)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON action payloads; results are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses read-only get and list actions.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
