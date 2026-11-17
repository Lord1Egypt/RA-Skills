## Description:

Guides video translation through LinkPix, with options for translated subtitles, dubbed audio, and lip synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and marketing teams use this skill to localize Chinese- or English-language videos for international audiences through translated subtitles, dubbing, and optional lip synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or updating qhkit can alter the local npm environment.

Mitigation: Review global npm installation and PATH changes before execution; prefer reviewed or pinned versions in sensitive environments.

Risk: The workflow requires a qhkit API token and uploads video files to an external service.

Mitigation: Use an approved token and upload only videos authorized for external processing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-video-translate)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Video links]

**Output Format:** [Markdown guidance with CLI commands and completed video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the task ID, completion status, and credits charged; videos are processed asynchronously.]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
