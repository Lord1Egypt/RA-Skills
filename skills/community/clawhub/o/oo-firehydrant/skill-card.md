## Description:

FireHydrant (firehydrant.com). Use this skill for ANY FireHydrant request — reading, creating, and updating data. Whenever a task involves FireHydrant, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and incident responders use the skill to read FireHydrant incidents, services, and environments, and to create incidents through a connected FireHydrant account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can make broader, persistent changes to other agents' skills.

Mitigation: Review and verify the CLI installation and its skill synchronization behavior; disable startup skill synchronization if only this integration is needed.

Risk: The remote installers and live connector behavior were not verified, so their exact behavior is uncertain.

Mitigation: Verify the CLI installation separately and review the live action schema before sending a request.

Risk: Creating an incident changes FireHydrant state.

Mitigation: Confirm the exact payload and effect with the user before running the create action.

## Reference(s):

- [FireHydrant API documentation](https://docs.firehydrant.com/reference/firehydrant-api)
- [FireHydrant](https://firehydrant.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use live action schemas; incident creation requires user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
