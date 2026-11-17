## Description:

Use an OOMOL-connected Harvest account to read, create, update, or delete Harvest data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to read Harvest clients, projects, tasks, time entries, and user details, and to manage time entries in a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup executes downloaded code without a separate approval step, and the installers and hosted implementation are unverified.

Mitigation: Independently obtain and verify the oo CLI, review setup changes to installed skills, and limit the connected Harvest account's permissions.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Harvest](https://www.getharvest.com)
- [Harvest API v2 authentication guide](https://help.getharvest.com/api-v2/authentication-api/authentication/authentication/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [oo CLI commands and JSON Harvest responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return Harvest account data; time-entry changes require user confirmation, and destructive actions require explicit approval.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
