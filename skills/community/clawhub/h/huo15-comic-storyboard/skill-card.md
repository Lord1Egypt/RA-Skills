## Description:

Generates one vertical comic storyboard key frame per scene from a script.json file and character-card references using Seedream 4.0 image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to turn comic or short-drama scene data into storyboard key frames while preserving character consistency through reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted character manifest could reference unintended local files for upload to the external image API.

Mitigation: Accept character manifests only from trusted sources, constrain reference image paths to the character directory, and reject symlinks, absolute paths, and traversal paths.

Risk: Prompts and character reference images are sent to Ark/Volcengine using ARK_API_KEY.

Mitigation: Treat prompts and reference images as external API data, validate image type and size before use, and avoid submitting sensitive or unapproved content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-comic-storyboard)
- [Volcengine Seedance documentation](https://www.volcengine.com/docs/82379/1520757)
- [Volcengine TTS documentation](https://www.volcengine.com/docs/6561/97465)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Images, JSON]

**Output Format:** [PNG storyboard frames and a JSON manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces vertical 9:16 frames at 768x1344, with per-scene prompts recorded in manifest.json.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
