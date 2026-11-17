## Description:

Creates GPT Image 2 oriented e-commerce product images from text prompts or optional reference images through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators, product photographers, brand teams, and livestream sellers can create product listing images, ads, posters, and social assets for marketplaces and storefronts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance requests an API key in chat, which could expose the credential.

Mitigation: Configure the key through a protected local credential mechanism; rotate any key already shared.

Risk: The setup can automatically install or update external software whose behavior and credential storage were not verified.

Mitigation: Review and pin dependencies before installation or upgrades.

Risk: Reference images are uploaded to Qinghu for processing.

Mitigation: Upload only reference images you intend the service to process.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-gpt-image-2)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Text, Shell commands]

**Output Format:** [Generated product images with prompt and command guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports optional reference images and configurable image count, size, and prompt.]

## Skill Version(s):

0.1.4 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
