## Description:

Helps create short product-promotion videos from product images and selling points, with generated scripts, voiceover, captions, and transitions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and merchants use this skill to turn product images and selling points into short videos for e-commerce and social media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may install or update qhkit and Node tooling on the host without a clear confirmation boundary.

Mitigation: Preinstall and pin the CLI yourself; require approval before host software changes.

Risk: Configuring an API token and uploading product media exposes credentials and files to the video service.

Mitigation: Confirm the service account and exact files before configuring credentials or uploading media.

Risk: Video generation spends account credits and submitted jobs cannot be canceled.

Mitigation: Confirm the model, duration, files, and estimated cost before submitting a job.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-sales-video)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with shell commands, task status, and video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports estimated and charged credits when available; generated media is delivered by URL.]

## Skill Version(s):

0.1.8 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
