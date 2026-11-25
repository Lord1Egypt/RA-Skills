## Description:

AIsa (aisa.one). Use this skill for ANY AIsa request — reading, creating, updating, and deleting data. Whenever a task involves AIsa, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using AIsa through an OOMOL-connected account can inspect available action schemas and perform tasks such as reading, creating, updating, or deleting AIsa data. The skill guides the agent to submit schema-matched requests through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions offer a remote installer whose behavior the security evidence says is unknown.

Mitigation: Review and verify the installer before running it; use an already installed oo CLI where possible.

Risk: Security analysis is partial because two local references were missing.

Mitigation: Locate and review the missing referenced material and complete the security review before relying on the skill.

Risk: The skill exposes actions that can create, update, or delete AIsa data.

Mitigation: Review the action schema and target data before making changes, and confirm destructive actions with the user.

## Reference(s):

- [AIsa API documentation](https://aisa.one/docs/zh/api-reference)
- [AIsa](https://aisa.one)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-aisa)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON]

**Output Format:** [oo CLI commands with JSON request payloads and connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inspect each action schema before building a request; actions may read or change AIsa data.]

## Skill Version(s):

1.0.6 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
