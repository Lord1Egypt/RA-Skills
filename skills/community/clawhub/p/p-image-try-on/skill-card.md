## Description:

Guides virtual try-on by dressing a person in garments from reference photos for fashion or ecommerce.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pruna-ai](https://clawhub.ai/user/pruna-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Fashion and ecommerce teams and other users can guide an agent to create virtual try-on images from a person photo and garment references through Pruna's API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Person, garment, or pose photos sent to the remote API may contain identifiable or sensitive information.

Mitigation: Upload only images you are authorized to send and review Pruna's privacy and retention terms before use.

Risk: Optional dependency installation targets are not pinned to a specific release.

Mitigation: Install only from a trusted Pruna source and consider pinning or verifying dependency targets before use.

## Reference(s):

- [p-image-try-on on ClawHub](https://clawhub.ai/pruna-ai/skills/p-image-try-on)
- [Virtual try-on example prompts](artifact/example-prompt.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance for uploading authorized reference images and requesting a generated try-on image from Pruna's API.]

## Skill Version(s):

1.0.15 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
