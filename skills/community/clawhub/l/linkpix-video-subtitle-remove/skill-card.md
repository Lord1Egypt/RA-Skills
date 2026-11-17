## Description:

Removes hardcoded subtitles from videos and repairs the affected frames using the LinkPix video-edit service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Video editors and content creators use this skill to remove embedded subtitles before translating or repurposing video footage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local videos are uploaded to the qhkit cloud service for processing.

Mitigation: Only submit videos you are authorized to share with the provider.

Risk: Using the service requires an API token and may install qhkit or Node locally.

Mitigation: Protect the token, prefer a reviewed or pinned qhkit version, and avoid permanent Node or PATH changes unless needed.

Risk: Submitted video tasks may consume credits and cannot be canceled.

Mitigation: Confirm the intended inputs and potential charges before submitting a task.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-video-subtitle-remove)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown with command examples and video result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides task status, resulting video URLs, and charged credits when available.]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
