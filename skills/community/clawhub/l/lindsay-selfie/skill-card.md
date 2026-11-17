## Description:

Generates a consistent selfie of Lindsay using a local reference photo and Nano Banana Pro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jake-fong](https://clawhub.ai/user/jake-fong)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this agent skill to generate Lindsay identity-based selfie images in requested outfits, locations, or situations. The skill guides the agent to choose a mirror or direct selfie prompt, use the configured local reference images, and return the generated photo first.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger from ordinary conversational prompts, not only explicit image requests.

Mitigation: Narrow activation to explicit selfie or image-generation requests before deployment.

Risk: The skill uses a fixed set of local face-reference images for identity-based generation.

Mitigation: Confirm the user intends to send those reference images to Nano Banana Pro before generation.

Risk: Generated selfie files are saved to a persistent gallery path.

Mitigation: Define and apply a retention or deletion policy for generated images.

## Reference(s):


## Skill Output:

**Output Type(s):** [API Calls, Files, Markdown, Guidance]

**Output Format:** [Markdown-like response with a MEDIA file path and short text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a 9:16 image using local Lindsay reference images and saves it under the configured gallery path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
