## Description:

Applies a print design to a product image to create a realistic ecommerce mockup, with the design following the product’s folds, lighting, and perspective.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

POD sellers and ecommerce designers use this skill to preview a print on garments, hats, mugs, and other products. It creates mockups from a print image and, when available, a product image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference images are sent to an external generation provider, whose storage practices are outside this review.

Mitigation: Only upload images you are comfortable sharing with that provider, and check its data handling terms.

Risk: The CLI uses an API key that could be exposed if mishandled.

Mitigation: Protect the key and avoid placing it in shared files or logs.

Risk: CLI upgrades can change behavior or dependencies.

Mitigation: Use a reviewed, pinned version and inspect upgrades before applying them.

Risk: Image generation may alter fine print details in the mockup.

Mitigation: Inspect the generated image and verify important design elements before delivery.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix POD workspace](https://www.iqinghu.com)
- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-pod-pattern-apply)

## Skill Output:

**Output Type(s):** [Image files, Text]

**Output Format:** [Generated product mockup images with a brief delivery message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated redraws can change print details; review key design elements before delivery.]

## Skill Version(s):

0.1.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
