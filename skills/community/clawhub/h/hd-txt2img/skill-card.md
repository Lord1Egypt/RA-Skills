## Description:

Call Hidream txt2img async API with exposed auth and request parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhihui-chen-xx](https://clawhub.ai/user/zhihui-chen-xx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate images from text prompts through Hidream's async txt2img API, including selecting allowed resolutions, supplying authorization, and polling task results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and API tokens are sent to Hidream when the skill is used.

Mitigation: Install and run the skill only when that data sharing is acceptable for the intended prompts and account.

Risk: Passing real API tokens directly in shell commands can expose them through shell history or process inspection.

Mitigation: Set HIDREAM_AUTHORIZATION through a protected environment or secret manager, rotate any token previously pasted into history, and use limited-scope tokens where supported.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhihui-chen-xx/skills/hd-txt2img)
- [ClawHub publisher profile](https://clawhub.ai/user/zhihui-chen-xx)
- [Hidream txt2img async API endpoint](https://www.hidreamai.com/api-pub/gw/v3/image/txt2img/async)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include allowed resolution values, authorization setup, polling guidance, and structured task results with task_id, request_id, images, and errors.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
