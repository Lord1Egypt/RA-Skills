## Description:

Provides AITable operations for reading, creating, updating, and deleting data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

AITable users and developers use this skill to inspect spaces, datasheets, fields, views, and records, and to create, update, or delete records through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback includes a remote CLI installer that has not been verified; the hosted runtime and installers remain unverified.

Mitigation: Review and approve CLI installation separately, preferably using a verified, fixed release, and check whether it installs additional agent skills.

Risk: Connecting AITable authorizes OOMOL to mediate access to account data, and write or delete actions can change that data.

Mitigation: Use a narrowly scoped account and retain the required approvals for changes and deletions.

## Reference(s):

- [AITable](https://aitable.ai)
- [AITable API documentation](https://developers.aitable.ai/api/reference/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [AITable ClawHub release](https://clawhub.ai/oomol/skills/oo-aitable-ai)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON inputs and connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Record create, update, and delete actions handle up to 10 records per call; changes and deletions require user confirmation.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
