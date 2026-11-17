## Description:

An AI commercial image-generation skill for creating single product images, replicating visual style from reference images, and generating cohesive image suites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lirule007](https://clawhub.ai/user/lirule007)

### License/Terms of Use:


## Use Case:

External users and commercial content teams use this skill to generate product imagery, reproduce a reference visual style for new product images, or create coordinated e-commerce image sets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, product descriptions, reference image URLs, and possible Base64 image data are sent to a disclosed remote Supabase service for processing.

Mitigation: Avoid confidential, regulated, or unreleased business assets unless the provider's retention and privacy terms are acceptable.

Risk: Generated commercial images may be unsuitable, inaccurate, or inconsistent with brand requirements.

Mitigation: Review generated images and enhanced prompts before publication or downstream use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lirule007/skills/pony-image)
- [Configured Supabase edge functions endpoint](https://vecarpahagopuqbwxbjh.supabase.co/functions/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to return generated image URLs or Base64 image data and enhanced prompts from the remote image service.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
