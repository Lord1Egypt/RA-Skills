## Description:

Guides an agent through removing watermarks or corner logos from up to 10 videos per request using LinkPix's qhkit video-edit service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and editors use this skill to remove watermarks or corner logos from their own or authorized video footage for media cleanup and reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Removing watermarks from someone else's video may infringe their rights.

Mitigation: Use only on videos you own or have permission to edit and reuse.

Risk: Local videos are uploaded to a third-party service for processing.

Mitigation: Submit only videos you are comfortable sharing with that service.

Risk: The workflow requires an API token and installation of a third-party npm CLI.

Mitigation: Protect the token and consider pinning the CLI package version in controlled environments.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-video-watermark-remove)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [iqinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration guidance, Video links]

**Output Format:** [Markdown with shell commands and task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports 1–10 input videos per request; completed tasks return processed-video URLs.]

## Skill Version(s):

0.1.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
