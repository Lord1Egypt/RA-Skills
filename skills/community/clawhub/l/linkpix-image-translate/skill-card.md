## Description:

Translates text in product images into other languages by generating redesigned images that aim to preserve the original layout and visual style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially cross-border e-commerce sellers, use the skill to localize product images for different markets. It guides image translation and batch generation while recommending review of important text and product details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images are uploaded to LinkPix for processing, which may expose private or sensitive content.

Mitigation: Upload only images you are comfortable sharing with LinkPix.

Risk: Installing or updating the CLI can introduce software supply or system configuration risks.

Mitigation: Prefer a reviewed package version, avoid administrator privileges, and check before replacing existing service configuration.

Risk: Generated redraws can contain translation errors or alter prices, logos, or product details.

Mitigation: Review each output, including translated text and other important product information, before use.

Risk: An API token could be exposed or mishandled.

Mitigation: Protect the API token and avoid sharing it in prompts or logs.

## Reference(s):

- [LinkPix qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-image-translate)

## Skill Output:

**Output Type(s):** [Images, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Generated image files and Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images may need review for text accuracy and changes to prices, logos, or product details.]

## Skill Version(s):

0.1.8 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
