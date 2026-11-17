## Description:

Creates JD product images, image sets, detail graphics, and campaign visuals through Qinghu AI using configured image models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators, advertising specialists, and brand teams use the skill to create JD product images, carousel sets, detail graphics, and campaign visuals from product references.

### Deployment Geography for Use:

China; the skill documents the domestic iqinghu.com service and JD-related marketplaces.

## Known Risks and Mitigations:

Risk: The skill's setup flow asks users to send an API key in chat, which could expose the credential.

Mitigation: Configure a narrowly scoped key locally through a protected credential mechanism; rotate any key already shared.

Risk: The setup and upgrade instructions install or update software without pinning its version.

Mitigation: Review and pin the CLI and compression tools before allowing automatic setup or upgrades.

Risk: Product reference images are sent for external processing, and image generation can incur usage costs.

Mitigation: Use only reference images approved for external processing and retain the cost-confirmation step.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix JD Image on ClawHub](https://clawhub.ai/autoagc/skills/linkpix-jd-image)

## Skill Output:

**Output Type(s):** [Images, Text]

**Output Format:** [Product image files or URLs with concise task status and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image count, size, model, platform, and reference images depend on the requested deliverable.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
