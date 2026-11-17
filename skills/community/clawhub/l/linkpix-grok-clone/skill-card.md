## Description:

Helps social media creators adapt a trending video's narrative structure to their own product and generate a new short video through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Social media creators and marketers use the skill to analyze a short-video reference, adapt its script and pacing to a product, and generate a new video for social platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install npm-based qhkit tooling on the user's machine.

Mitigation: Review and approve the package installation before running the skill.

Risk: The remote service uses an API key and receives submitted media or links.

Mitigation: Keep the API key private and submit only media and links approved for upload.

Risk: Generating a video consumes paid credits.

Mitigation: Confirm the generation parameters and estimated charge with the user before submission.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-grok-clone)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key guide](https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g)

## Skill Output:

**Output Type(s):** [Text, Markdown, Video links]

**Output Format:** [Markdown with an original/adapted script comparison and generated video URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the task status and credits charged when available.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
