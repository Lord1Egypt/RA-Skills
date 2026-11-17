## Description:

Guides agents in creating e-commerce product videos, multi-image promotional clips, and storyboards using qhkit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and marketing teams use this skill to guide an agent in preparing product-video prompts and storyboards, estimating generation costs, and delivering completed promotional videos.

### Deployment Geography for Use:

Global (this release targets the China-based iqinghu.com service).

## Known Risks and Mitigations:

Risk: Installing and running an external qhkit CLI introduces a software dependency.

Mitigation: Install only if the service is trusted and prefer a reviewed or pinned qhkit version.

Risk: Selected product images or videos are uploaded to the service.

Mitigation: Confirm the user is comfortable sharing each selected media asset before submission.

Risk: API tokens and video generation with paid credits require user authorization.

Mitigation: Keep tokens private, check the estimate when available, and obtain approval before incurring charges.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/linkpix-ecom-video)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu workbench](https://www.iqinghu.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with qhkit command examples and video-result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation is asynchronous; completed videos are provided as links after status checks.]

## Skill Version(s):

0.1.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
