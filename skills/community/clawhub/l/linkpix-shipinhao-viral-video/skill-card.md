## Description:

Guides agents in creating WeChat Channels promotional videos with qhkit, including media selection, cost review, task tracking, and delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, merchants, and livestream teams use this skill to plan and generate short product, storytelling, and promotional videos for WeChat Channels and related social placements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or upgrading qhkit and adjusting a user-level PATH changes the local tool environment.

Mitigation: Review installation steps, prefer a pinned qhkit version, and approve any PATH changes before applying them.

Risk: Selected media and a qhkit API key are sent to the video provider.

Mitigation: Upload only approved media and manage the API key as a secret.

Risk: Video generation consumes credits and submitted tasks cannot be cancelled.

Mitigation: Review the model, duration, reference media, language, and estimated credits, then obtain explicit approval before submission.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-shipinhao-viral-video)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu AI API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Video links]

**Output Format:** [Markdown with command examples and generated-video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically recommends portrait 9:16 video in Simplified Chinese; generation returns a task ID before a video link is available.]

## Skill Version(s):

0.1.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
