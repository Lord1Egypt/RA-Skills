## Description:

Generate identity-consistent selfies, group photos, and other SFW images for OpenClaw characters via the tuqu.ai API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouyi531](https://clawhub.ai/user/zhouyi531)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to generate character-consistent portraits, selfies, group images, preset-based images, and SFW edit-only images through tuqu.ai.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Service keys and image data can be sent to custom hosts through base URL overrides or absolute endpoint paths.

Mitigation: Use the default tuqu.ai hosts unless there is a documented trusted-host reason, and protect role-specific service keys.

Risk: Deletion, recharge, and payment flows can affect saved characters, history, balances, or checkout state.

Mitigation: Require manual confirmation before delete, recharge, or payment actions, and preserve returned IDs and payment artifacts for review.

## Reference(s):

- [OpenClaw Selfie on ClawHub](https://clawhub.ai/zhouyi531/skills/openclaw-selfie)
- [Tuqu API Notes](TUQU_API.md)
- [Endpoint Reference](references/endpoints.md)
- [Workflow Recipes](references/workflows.md)
- [tuqu.ai](https://tuqu.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request or response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to call tuqu.ai photo and billing endpoints with a role-specific service key.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
