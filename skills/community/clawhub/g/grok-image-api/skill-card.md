## Description:

Work with OpenAI-compatible image generation and image editing endpoints for prompt-based image generation, prompt-guided image editing with optional masks, endpoint testing, and integration with /v1/images/generations or /v1/images/edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaolozee](https://clawhub.ai/user/xiaolozee)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to call OpenAI-compatible image generation and image editing APIs, save generated or edited images locally, and integrate those image endpoints into scripts or workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A remote or misconfigured API endpoint may receive credentials, prompts, and uploaded images.

Mitigation: Use only a trusted HTTPS API base URL, keep API keys scoped and revocable, and avoid sending sensitive prompts or images.

Risk: Returned image URLs may be downloaded and saved locally by default.

Mitigation: Use a controlled output path or request URL retention when local persistence is not appropriate.

## Reference(s):

- [API notes](artifact/references/api-notes.md)
- [ClawHub skill page](https://clawhub.ai/xiaolozee/skills/grok-image-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated or edited image files locally, or return a remote image URL when requested.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
