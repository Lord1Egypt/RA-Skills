## Description:

Helps social media marketers adapt the structure of popular short videos into product video scripts and generate Seedance 2.0 videos through the Qinghu AI service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Social media and ecommerce marketers use this skill to analyze a reference short video, adapt its pacing and shot structure for their product, and generate a promotional video after approving the script and estimated credit cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic installation or updates of unpinned Node and qhkit tooling may introduce unreviewed code.

Mitigation: Use a disposable workspace and preinstall a reviewed qhkit version when possible.

Risk: Service credentials and reference media may be stored locally or sent to the Qinghu AI service.

Mitigation: Protect the API token and avoid uploading sensitive videos or product images.

Risk: Generating a video spends credits and the task cannot be canceled after submission.

Mitigation: Check the quoted credit cost and generation parameters, then obtain explicit approval before submitting.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/linkpix-seedance-2-clone)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Video links]

**Output Format:** [Markdown with script comparison, task status, and generated video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports estimated credits before generation and actual credits upon delivery.]

## Skill Version(s):

0.1.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
