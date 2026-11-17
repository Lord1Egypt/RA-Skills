## Description:

Google Model Armor: Sanitize a model response through a Model Armor template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to sanitize outbound model responses through a configured Google Model Armor template using the gws CLI. It is intended for model-to-user response safety checks before content is returned downstream.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Response text or JSON supplied to the command may be sent to the configured Google Model Armor service or template.

Mitigation: Confirm the target Model Armor configuration and data handling requirements before using --text or --json with sensitive content.

Risk: The workflow depends on the gws CLI and the referenced gws-shared skill for authentication, global flags, and security rules.

Mitigation: Install only a trusted gws CLI and verify that gws-shared is present and acceptable in the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-modelarmor-sanitize-response)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash commands, CLI flags, examples, and operational notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI, the gws-shared skill, and a full Model Armor template resource name; accepts response content through --text or --json.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
