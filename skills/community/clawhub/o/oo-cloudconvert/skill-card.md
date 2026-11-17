## Description:

CloudConvert (cloudconvert.com). Use this skill for ANY CloudConvert request — reading, creating, updating, and deleting data. Whenever a task involves CloudConvert, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other CloudConvert users can manage conversion jobs and tasks through an OOMOL-connected account. The skill provides guidance for inspecting action schemas and running read, write, and destructive operations with the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can run downloaded installation code without asking.

Mitigation: Review and approve CLI installation separately, using a pinned and verified release.

Risk: Additional agent skills may be synchronized during setup.

Mitigation: Review whether skill synchronization is appropriate; the documented OO_SKILLS_SYNC_DISABLED setting disables it.

Risk: Write and destructive actions can change or delete CloudConvert data.

Mitigation: Inspect the action schema and exact payload, then obtain user approval before running write or destructive actions.

## Reference(s):

- [CloudConvert](https://cloudconvert.com)
- [CloudConvert API documentation](https://cloudconvert.com/api/v2)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with oo CLI commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
