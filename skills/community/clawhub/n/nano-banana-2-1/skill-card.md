## Description:

Generate and edit images with Google's Nano Banana 2.1 through the PopNow API: text-to-image and multi-image edits up to 4K, sharp in-image text, web-grounded drawing, exact USD quotes before any charge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyuminjo](https://clawhub.ai/user/kyuminjo)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and developers can create new images or edit one or more reference images with Nano Banana 2.1. The skill obtains an exact price quote and requires approval before paid generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid image generation can incur API charges.

Mitigation: Use a dedicated PopNow key with model restrictions and spending caps, and approve each quoted maximum before generation.

Risk: Prompts and reference URLs are sent to external providers and may appear in host logs.

Mitigation: Avoid including sensitive material in prompts or reference URLs.

## Reference(s):

- [Nano Banana 2.1 model page](https://popnow.ai/models/nano-banana-2-1)
- [PopNow task API documentation](https://popnow.ai/docs/tasks)

## Skill Output:

**Output Type(s):** [Images, Guidance]

**Output Format:** [Generated image output links with concise task status and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text-to-image and multi-image edits, with resolutions up to 4K.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
