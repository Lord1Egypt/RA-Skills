## Description:

Generates or edits images from text prompts or source images through APIYI's NanoBanana2 proxy service, with selectable aspect ratios and 1K, 2K, or 4K resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate new images or edit existing images from natural-language prompts, including social media assets, marketing visuals, wallpapers, posters, and image restoration or style-transfer tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected source images are sent to APIYI's remote service.

Mitigation: Avoid confidential prompt text and sensitive images unless that remote processing is acceptable for the use case.

Risk: API keys may be exposed if passed directly on the command line.

Mitigation: Use the APIYI_API_KEY environment variable instead of command-line key arguments when possible.

Risk: Generated output paths are local file writes controlled by command arguments.

Mitigation: Review output filenames and directories before execution to avoid overwriting or writing files in unintended locations.

## Reference(s):

- [Common use scenarios](references/scene.md)
- [APIYI service](https://api.apiyi.com/)
- [ClawHub skill page](https://clawhub.ai/wuchubuzai2018/skills/nano-banana-2-image-gen)

## Skill Output:

**Output Type(s):** [guidance, shell commands, files]

**Output Format:** [Markdown guidance with shell commands and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIYI_API_KEY; generated or edited images are written to local output paths chosen by the command arguments.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
