## Description:

Generates e-commerce sales scripts from product details or a reference video, including spoken pitches, recommendations, reviews, and story-driven formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and marketers use this skill to draft product-focused sales copy and video scripts or adapt ideas from a reference video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may install or update npm tooling without sufficient user oversight.

Mitigation: Approve tooling changes before execution and prefer a preinstalled, pinned qhkit version.

Risk: Configuring qhkit may expose or persist service credentials.

Mitigation: Provide tokens through a secure secret mechanism and limit credential handling to the required service.

Risk: Referenced product images or videos may be uploaded to the qhkit/iqinghu service.

Mitigation: Confirm permission to share product media before submitting it to the service.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/linkpix-sales-script)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Text script in an agent response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full script delivered in the response; reference-video generation may require polling.]

## Skill Version(s):

0.1.6 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
