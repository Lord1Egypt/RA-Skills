## Description:

Use this skill for any DeskTime request involving reading, creating, or updating data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees can use this skill to read company, employee, and project data from a connected DeskTime account, and to create projects or associated tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup instructions can run downloaded code without a separate approval step; the remote installers and exact installed release were not inspected.

Mitigation: Install a verified CLI release yourself, review installers before running them, and prevent automatic installer execution.

Risk: DeskTime access may expose employee tracking data.

Mitigation: Review managed-skill synchronization settings and authorize only the DeskTime access needed.

Risk: Creating a project or associated task changes DeskTime data.

Mitigation: Confirm the exact payload and effect with the user before running a write action.

## Reference(s):

- [DeskTime](https://desktime.com/)
- [DeskTime API documentation](https://help.desktime.com/hc/en-us/articles/25494558790685-Introduction-to-the-DeskTime-API)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON action payloads and DeskTime response data, with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read company, employee, and project data; project creation can also create an associated task. Write actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
