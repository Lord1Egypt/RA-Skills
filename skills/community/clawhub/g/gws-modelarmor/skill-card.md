## Description:

Google Model Armor: Filter user-generated content for safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and run Google Model Armor commands that filter user prompts and model responses for safety.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and responses processed with Model Armor may be shared with that service.

Mitigation: Confirm the intended Google Cloud project and credentials before use, and treat submitted prompts and responses according to the organization's data handling policy.

Risk: Helper skills for template creation or sanitization may add behavior beyond this wrapper skill.

Mitigation: Review helper skills separately before relying on their commands in a workflow.

## Reference(s):

- [Gws Modelarmor on ClawHub](https://clawhub.ai/googleworkspace-bot/skills/gws-modelarmor)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and intended Google Cloud credentials.]

## Skill Version(s):

1.0.12 (source: server release evidence); 0.22.5 (source: skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
