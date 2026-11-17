## Description:

Use the OOMOL-connected Paymo account to read, create, update, and delete Paymo data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can operate a Paymo account connected through OOMOL to retrieve clients, projects, tasks, and the current user, or create, update, and delete clients, projects, and tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The missing-software fallback runs remote installers without clearly obtaining permission for broader local changes.

Mitigation: Review the installer and automatic agent-skill installation settings before using the fallback setup steps.

Risk: Paymo write and destructive actions can change or remove account data.

Mitigation: Keep approval checks for changes and get explicit confirmation of the target before deletions.

## Reference(s):

- [Paymo skill page](https://clawhub.ai/oomol/skills/oo-paymo)
- [Paymo](https://www.paymoapp.com)
- [Paymo API documentation](https://github.com/paymoapp/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON payloads and explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions can run directly; changes require approval and deletions require explicit confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
