## Description:

CallPage (callpage.io). Use this skill for ANY CallPage request — reading, creating, and updating data. Whenever a task involves CallPage, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

CallPage users use the skill to list and retrieve call, user, and widget records, and to create callback requests through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote code and introduce persistent agent changes without clear approval.

Mitigation: Review and install a verified oo CLI release, and check its automatic skill installation and synchronization settings before use.

Risk: Creating a callback request changes CallPage state.

Mitigation: Confirm the callback details, including its widget and phone number, before submitting the request.

## Reference(s):

- [CallPage REST API documentation](https://callpage.github.io/documentation-rest/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [CallPage ClawHub release](https://clawhub.ai/oomol/skills/oo-callpage)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands]

**Output Format:** [JSON API responses and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include action data and an execution ID.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
