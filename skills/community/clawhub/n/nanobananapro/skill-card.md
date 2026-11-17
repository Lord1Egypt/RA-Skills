## Description:

Generate/edit images with Nano Banana Pro (Gemini 3 Pro Image). Use for image create/modify requests incl. edits. Supports text-to-image + image-to-image; 1K/2K/4K; use --input-image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youthzenith](https://clawhub.ai/user/youthzenith)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use this skill to generate new images from text prompts or edit existing images with targeted instructions. It guides an agent through Gemini API key setup, resolution choices, prompt handling, and saving generated PNG files in the user's working directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and input images are sent to Google's Gemini image service.

Mitigation: Use the skill only with content that is appropriate to share with that service, and review applicable data handling requirements before use.

Risk: API keys can be exposed if pasted into chat or command arguments.

Mitigation: Prefer setting GEMINI_API_KEY in a protected environment and avoid sharing credentials in conversation history or shell history.

Risk: Running with uv may fetch dependency versions at execution time.

Mitigation: Review dependency resolution in controlled environments and pin or lock dependencies where deployment policy requires reproducibility.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youthzenith/skills/nanobananapro)
- [Publisher profile](https://clawhub.ai/user/youthzenith)

## Skill Output:

**Output Type(s):** [guidance, shell commands, files]

**Output Format:** [Markdown guidance with inline bash commands; generated PNG image files when the helper script runs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text-to-image and image-to-image workflows with 1K, 2K, and 4K resolution options. Requires a Gemini API key.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
