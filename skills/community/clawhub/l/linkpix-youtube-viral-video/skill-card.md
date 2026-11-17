## Description:

Helps creators and marketing teams plan and generate YouTube product videos, reviews, and ads with the qhkit video service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Brand marketers, creators, and ad teams use this skill to plan and generate YouTube product demonstrations, reviews, branded ads, and Shorts from prompts and supplied media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or upgrading Node/npm and an unpinned qhkit package can change the local environment.

Mitigation: Review installation steps and prefer an already installed, pinned qhkit version.

Risk: Selected images or videos may be uploaded to the qhkit service.

Mitigation: Confirm which media may be shared before submitting a generation task.

Risk: An API key may be stored locally or exposed if pasted into chat or shell history.

Mitigation: Provide credentials through a secure secret mechanism rather than pasting a long-lived key into chat or commands.

Risk: Video generation consumes credits and submitted tasks cannot be canceled.

Mitigation: Show the selected settings and estimated charge, then obtain explicit approval before submission.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-youtube-viral-video)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu AI API key setup](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with video links and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports task status and credit usage; generated video links are supplied when ready.]

## Skill Version(s):

0.1.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
