## Description:

Replaces the person in product images or videos for ecommerce localization, with image workflows designed to preserve the original clothing and pose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams can localize product imagery and video by replacing a model with a reference person or a described appearance. The workflow requires authorization for real-person likenesses and recommends checking generated media for changes to important product details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected photos and videos are uploaded to a cloud service for processing.

Mitigation: Use the service only with media you are authorized to share, and proceed only if you trust the provider with those files.

Risk: The workflow uses an API key and installs or updates a command-line package.

Mitigation: Use a reviewed, pinned package version, review upgrades before running them, avoid elevated installation where possible, and protect the API key.

Risk: Replacing a real person's face without permission can misuse their likeness; generated redraws can also alter product details.

Mitigation: Confirm authorization before processing real-person likenesses, refuse unauthorized requests, and inspect generated media for text, logos, and product structure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/linkpix-model-face-swap)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Videos, Text]

**Output Format:** [Generated image or video files with result links, plus concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated redraws may slightly change subject details; review text, logos, and product structure in the results.]

## Skill Version(s):

0.1.8 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
