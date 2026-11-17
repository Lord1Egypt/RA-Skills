## Description:

Optimizes e-commerce product hero images by improving composition, lighting, texture, and detail to increase visual appeal and click-through potential.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce sellers and agents use this skill to improve an existing product hero image, address visual issues such as lighting or texture, or generate a coordinated set of revised product images. Because generation redraws the image, users should check important product details in the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs automatic global CLI upgrades and may execute upgrade commands returned at runtime.

Mitigation: Pin the CLI to a reviewed version and inspect upgrade commands before approving and executing them.

Risk: Images submitted for processing may be handled by an external service, and image-retention practices are unverified.

Mitigation: Submit only images approved for external processing and use a dedicated service token.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/autoagc/skills/linkpix-main-image-optimize)
- [qhkit package on npm](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Image files, Guidance, Shell commands]

**Output Format:** [Generated product image files and concise Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation may slightly change product details; check text, logos, and product structure in generated images.]

## Skill Version(s):

0.1.8 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
