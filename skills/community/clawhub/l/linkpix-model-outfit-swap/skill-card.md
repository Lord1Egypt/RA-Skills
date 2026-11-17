## Description:

Creates virtual try-on images from clothing photos, optionally placing the clothing on a supplied model photo and allowing model characteristics to be specified.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Clothing sellers and ecommerce content creators use this skill to turn flat-lay or hanging garment photos into model try-on images, or to show a garment on a supplied model. Users can specify model characteristics and should review generated product details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded clothing or model photos may be sensitive, and provider retention practices are not verified.

Mitigation: Upload only photos you are authorized to use, and review LinkPix/iqinghu privacy terms before submitting sensitive images.

Risk: Setup may change qhkit credentials or site settings, and installation or automatic upgrades affect the local command-line tool.

Mitigation: Review the qhkit version and configuration before setup or upgrades, and protect account credentials.

Risk: Image generation consumes account credits.

Mitigation: Check the expected credit cost and account balance before generating images.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-model-outfit-swap)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Shell commands, Guidance]

**Output Format:** [Generated image files with shell command examples and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports clothing photos with an optional model photo and one or more generated image variations. Review garment details such as text, logos, and construction.]

## Skill Version(s):

0.1.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
