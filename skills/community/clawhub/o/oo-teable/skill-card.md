## Description:

Operate Teable through an OOMOL-connected account for reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to inspect Teable workspaces and records, and to create, update, or delete records through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run remote CLI software and additional agent skills that have not been inspected.

Mitigation: Review, approve, and verify the CLI and any additional skills separately before installing or running them.

Risk: The connected Teable account can expose or change workspace data.

Mitigation: Limit the connection to the permissions needed and retain the documented confirmation steps for edits and deletions.

## Reference(s):

- [Teable](https://teable.cn)
- [Teable API documentation](https://help.teable.cn/zh/api-doc/overview)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls, Shell commands]

**Output Format:** [Natural-language responses with oo CLI commands and JSON payloads when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read Teable data or propose changes; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
