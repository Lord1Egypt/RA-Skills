## Description:

Generate OpenClaw-themed X article cover images with a fixed composition: lobster logo on the right quarter and text zone on the left three quarters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunhe-dev](https://clawhub.ai/user/yunhe-dev)

### License/Terms of Use:


## Use Case:

External creators, marketers, and developers use this skill to generate OpenClaw-themed X article cover images from a required title and reference image while preserving the intended logo placement and readable text area.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cover titles, subtitles, and reference images are sent to the BLT image-generation API.

Mitigation: Use only authorized, non-sensitive prompts and reference images, and confirm the user is comfortable sharing them with the third-party API.

Risk: The script can create output directories and overwrite files at the chosen output path.

Mitigation: Choose a dedicated output path and review existing files before running generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yunhe-dev/skills/openclaw-x-article-cover-generator)
- [BLT image generation API endpoint](https://api.bltcy.ai/v1)

## Skill Output:

**Output Type(s):** [Files, Shell commands, API Calls, Guidance]

**Output Format:** [Generated image file saved locally with command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a title, a local or URL reference image, an output path, and BLT_API_KEY or an explicit API key.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
