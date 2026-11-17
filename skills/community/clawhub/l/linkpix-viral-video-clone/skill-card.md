## Description:

Analyzes a short-video link, adapts its script to the user's product, and helps generate a similarly styled marketing video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and marketers use this skill to adapt the structure and pacing of a short video into a product-specific script and generated marketing video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or upgrade Node and qhkit tooling globally without a clear consent gate.

Mitigation: Review and approve installation or upgrades before running them.

Risk: Configuring qhkit may persist an API token.

Mitigation: Confirm credential storage and scope before providing or configuring a token.

Risk: Provided images or reference videos may be uploaded to the service.

Mitigation: Review the media and obtain permission before uploading it.

Risk: Generated videos may consume service credits.

Mitigation: Review the estimated cost and adapted script with the user before submitting a paid generation task.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-viral-video-clone)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [iqinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Video links]

**Output Format:** [Markdown with an adapted script and a link to the generated video]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation is asynchronous and may spend service credits.]

## Skill Version(s):

0.1.8 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
