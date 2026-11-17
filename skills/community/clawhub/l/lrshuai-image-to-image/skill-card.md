## Description:

Generates new images from a reference image and text prompt using supported image-generation models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrshu](https://clawhub.ai/user/lrshu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to generate or transform images by sending a prompt plus optional reference media to a configured image-generation API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send prompts, selected local media, and TEAM_API_KEY-authenticated requests to a configurable remote API host.

Mitigation: Use only with media intended for that provider, scope TEAM_API_KEY appropriately, and confirm TEAM_BASE_URL before execution.

Risk: The release evidence reports that the skill bypasses the normal OpenClaw runner.

Mitigation: Review the script before use and prefer a release that uses the standard runner or an approved execution wrapper.

Risk: The security guidance notes missing disclosure or enforcement for allowed models, media types, file sizes, and request timeouts.

Mitigation: Run in a controlled environment and prefer a version that validates media inputs, limits model choices, and adds bounded request timeouts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrshu/skills/lrshuai-image-to-image)
- [Publisher profile](https://clawhub.ai/user/lrshu)
- [Configured API endpoint](https://dlazy.com/api/ai/tool)

## Skill Output:

**Output Type(s):** [shell commands, JSON, text, configuration]

**Output Format:** [Command-line output containing request status, errors, or API response JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TEAM_API_KEY and Python; may read selected local media paths and send encoded media to the configured API host.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
