## Description:

High quality AI image generation via the WellAPI gpt-image-2 model. Supports text-to-image and image editing (image-to-image).

This skill is ready for commercial/non-commercial use.

## Publisher:

[laolujava](https://clawhub.ai/user/laolujava)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to generate images from text prompts and edit local images through WellAPI's OpenAI-compatible image endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user prompts, selected local images, masks, and the WellAPI API key to WellAPI.

Mitigation: Use it only after reviewing WellAPI privacy, retention, and pricing terms, and avoid sensitive or regulated images unless that review is complete.

Risk: The fallback onboarding flow asks users to paste an API key and includes a registration link with channel tracking.

Mitigation: Prefer setting WELLAPI_API_KEY through an environment variable or secret mechanism, and review the tracked registration link before relying on the fallback prompt.

Risk: Generated images are saved locally and auto-attached to the conversation.

Mitigation: Confirm the output path and attachment behavior before generating sensitive images or sharing the conversation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laolujava/skills/image-generation-gpt)
- [WellAPI provider](https://wellapi.ai)
- [Python reference implementation](references/python.md)
- [PowerShell reference implementation](references/powershell.md)
- [curl and bash reference implementation](references/curl_heredoc.md)
- [Basic text-to-image example](examples/basic.md)
- [Advanced image editing example](examples/advanced.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions]

**Output Format:** [PNG, JPEG, or WebP image files with MEDIA:<absolute_path> text lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decodes synchronous base64 image responses, saves sanitized local filenames, and can return up to 10 images per request.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog list 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
