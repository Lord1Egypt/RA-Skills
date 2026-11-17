## Description:

Generate images, refine prompts, and search earlier results through a Huajing image-generation server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[starrysea1412](https://clawhub.ai/user/starrysea1412)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to refine image prompts, request images from a configured Huajing server, and retrieve images from its gallery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, generation requests, provider choices, and gallery queries go to the configured Huajing endpoint.

Mitigation: Use only a Huajing server endpoint you run or trust, and review content before sending it.

Risk: Results can include absolute local file paths when HUAJING_DATA_DIR is set.

Mitigation: Leave HUAJING_DATA_DIR unset unless file paths are needed, and avoid sharing results that expose local paths.

## Reference(s):

- [Huajing (AI Image Studio)](https://gitee.com/starry-sea-1412/ai-image-studio)

## Skill Output:

**Output Type(s):** [Text, Image URLs, Guidance]

**Output Format:** [JSON by default; optional plain text with image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images remain in the Huajing gallery; results may include local file paths when configured.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
