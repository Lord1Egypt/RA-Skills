## Description:

Guides agents in generating cinematic product and brand advertising videos through LinkPix using reference images and directed prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Brand teams and creators use this skill to plan and generate cinematic product ads and promotional video clips from product images and creative prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or invoking the third-party qhkit package can change the local environment.

Mitigation: Review the package and approve installation and environment changes before first use.

Risk: Media supplied to the skill is uploaded to the video-generation service.

Mitigation: Only submit media that the user has approved for upload.

Risk: Video generation can spend service credits.

Mitigation: Estimate credits before generating and confirm the cost with the user.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-ad-film)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix API key settings](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown with shell commands and completed video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation responses include task status, video URLs and credits spent.]

## Skill Version(s):

0.1.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
