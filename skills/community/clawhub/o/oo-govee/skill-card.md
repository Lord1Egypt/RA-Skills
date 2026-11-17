## Description:

Govee (govee.com). Use this skill for ANY Govee request — reading, creating, updating, and deleting data. Whenever a task involves Govee, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to inspect Govee devices and scenes, read device state, and control device capabilities through their connected Govee account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can execute remote installer code whose contents are unverified.

Mitigation: Review the CLI installer separately before setup and consider setting OO_SKILLS_SYNC_DISABLED=1 to prevent startup writes into agent skill directories; review any previously installed bundled skills.

Risk: A device control action can change Govee device state.

Mitigation: Keep explicit approval for device changes.

## Reference(s):

- [Govee API documentation](https://developer.govee.com/docs/getting-started)
- [oo CLI command controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Govee](https://www.govee.com)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON connector responses and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned device and scene data depends on the selected Govee action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
