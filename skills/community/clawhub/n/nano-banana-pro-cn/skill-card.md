## Description:

Generates and edits images from natural-language prompts through the APIYI-hosted NanoBananaPro image service, with support for multiple aspect ratios, 1K to 4K output sizes, and optional image inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content creators use this skill to generate new images or edit existing images from prompts for social content, marketing assets, wallpapers, illustrations, and image repair workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local input-image paths supplied to the script to the APIYI service, and scanner evidence notes it does not validate that those paths are actually images.

Mitigation: Use only non-sensitive images, verify each input path before execution, and run the skill in a restricted workspace that cannot read credentials, private keys, or unrelated documents.

Risk: API keys may be provided by command-line flag, which can expose credentials through shell history or process listings.

Mitigation: Prefer the APIYI_API_KEY environment variable and avoid passing API keys directly on the command line.

Risk: Prompts and image inputs are sent to a third-party provider for processing.

Mitigation: Confirm that APIYI is the intended backend before use and avoid sending private, regulated, or confidential content.

## Reference(s):

- [Common Usage Scenarios](references/scene.md)
- [APIYI Service](https://apiyi.com/)
- [APIYI API Console](https://api.apiyi.com)
- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/skills/nano-banana-pro-cn)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG image files with terminal status text and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text-to-image and image editing with optional aspect ratio, resolution, and up to 14 input images.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
