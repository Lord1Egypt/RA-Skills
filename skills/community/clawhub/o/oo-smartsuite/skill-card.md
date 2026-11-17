## Description:

Use SmartSuite through an OOMOL-connected account to read, create, update, or delete SmartSuite data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to access SmartSuite solutions, tables, and records through a connected account. It guides listing and retrieving data, and creating, updating, or deleting records with approval required for writes and deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can run downloaded CLI installers, and the external installer behavior is unverified.

Mitigation: Review and verify the oo CLI release before installing it, and require approval for installation and subsequent installation changes.

Risk: The connected account can be used to change or delete SmartSuite records.

Mitigation: Follow the skill's approval requirement and confirm the exact target and effect before running record changes or deletions.

## Reference(s):

- [SmartSuite](https://www.smartsuite.com/)
- [SmartSuite API authentication documentation](https://developers.smartsuite.com/docs/authentication)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas guide request payloads; record creation, updates, and deletions require user approval.]

## Skill Version(s):

1.0.5 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
