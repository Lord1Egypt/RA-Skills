## Description:

Converts a PowerPoint file on macOS into per-slide PNG images and 3x3 thumbnail sheets, then creates a WeChat official account draft using user-provided credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxm8023](https://clawhub.ai/user/zhaoxm8023)

### License/Terms of Use:


## Use Case:

Developers and content operators use this skill to automate macOS PowerPoint screenshot generation, thumbnail creation, markdown gallery output, and WeChat draft creation for presentation-based publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat credentials may be exposed if users paste real app IDs or secrets into chat, prompts, or config files.

Mitigation: Use environment variables or a secret manager, keep real credentials out of shared prompts and committed config files, and rotate any credential already shared.

Risk: Local presentation content may be uploaded to WeChat without a clear final confirmation step.

Mitigation: Review generated images and require explicit confirmation before upload or draft creation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoxm8023/skills/ppt2wechat)
- [Publisher profile](https://clawhub.ai/user/zhaoxm8023)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python script and JSON configuration artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local PNG files, thumbnail grids, a markdown image gallery, and a WeChat draft through external command-line tools and WeChat API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
