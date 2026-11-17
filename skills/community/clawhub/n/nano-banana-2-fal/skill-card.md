## Description:

Generate or edit images via Gemini 3 Pro Image (Nano Banana Pro).

This skill is ready for commercial/non-commercial use.

## Publisher:

[wingchiu](https://clawhub.ai/user/wingchiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate new images, edit a single image, or compose up to 14 input images through Google's Gemini image API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected input images are sent to Google's Gemini API.

Mitigation: Install only when this external API use is acceptable for the intended data, and avoid sending sensitive prompts or images unless approved.

Risk: API keys can be exposed if passed directly on the command line.

Mitigation: Prefer GEMINI_API_KEY or protected OpenClaw configuration instead of command-line key arguments.

Risk: Unpinned uv dependencies can reduce reproducibility.

Mitigation: Pin or lock dependencies for controlled deployments.

## Reference(s):

- [Google AI Developer Documentation](https://ai.google.dev/)
- [ClawHub Skill Page](https://clawhub.ai/wingchiu/skills/nano-banana-2-fal)
- [ClawHub Publisher Profile](https://clawhub.ai/user/wingchiu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown with bash commands, configuration notes, and generated PNG file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes PNG files and prints MEDIA attachment paths; supports 1K, 2K, and 4K image resolutions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
