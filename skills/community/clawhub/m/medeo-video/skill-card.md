## Description:

AI-powered video generation skill for generating videos from text descriptions, browsing video recipes, uploading assets, and managing video creation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnykui](https://clawhub.ai/user/sunnykui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate videos from text or supplied media, browse reusable video templates, upload assets, and deliver completed videos through supported chat platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags review-worthy risks around command execution, credential handling, external messaging, and unrestricted URL fetching.

Mitigation: Review carefully before installing, use scoped Medeo and chat-platform credentials, and deploy only in environments appropriate for this workflow.

Risk: Untrusted prompts or URLs may increase exposure to command-construction and URL-fetch issues.

Mitigation: Restrict use by untrusted users until those issues are fixed, avoid sending API keys in ordinary chat, and rotate any token that may appear in logs.

## Reference(s):

- [Medeo Video ClawHub Page](https://clawhub.ai/sunnykui/skills/medeo-video)
- [Medeo Platform](https://medeo.app)
- [Medeo API Docs](https://docs.prd.medeo.app/)
- [Recipes Guide](docs/recipes.md)
- [Uploading Assets](docs/assets-upload.md)
- [Feishu Video Delivery](docs/feishu-send.md)
- [Multi-Platform Video Delivery](docs/multi-platform.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs; generated videos are delivered as files or links through the user's chat platform.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation is asynchronous, requires a Medeo API key, and may use scoped chat-platform credentials for native delivery.]

## Skill Version(s):

1.5.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
