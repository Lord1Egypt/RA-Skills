## Description:

Generates Lazada-ready product image sets, detail-page visuals, and campaign posters with Southeast Asian localization through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Lazada sellers and Southeast Asian ecommerce teams use this skill to create platform-adapted product image sets, detail-page visuals, and promotional posters localized for markets such as Indonesia, Thailand, and the Philippines.

### Deployment Geography for Use:

Southeast Asia (including Indonesia, Thailand, and the Philippines)

## Known Risks and Mitigations:

Risk: The security review flags that the skill requests API keys through chat and automatically installs or upgrades executable tools.

Mitigation: Set the API key through a protected local secret mechanism, rotate any key already shared, and review and pin executable dependencies before installation or upgrades.

Risk: Reference images may be processed by Qinghu and its model providers, and external package behavior and service retention are unverified; image generation can also incur cost.

Mitigation: Confirm that the images may be processed by those providers and approve the generation cost before use.

## Reference(s):

- [QHKit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix Lazada skill on ClawHub](https://clawhub.ai/autoagc/skills/linkpix-lazada-image)

## Skill Output:

**Output Type(s):** [Images, Shell commands, Guidance]

**Output Format:** [Generated image files or URLs, with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product main-image sets, detail-page visuals, and campaign posters; options and model labels are selected from the service's current choices.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
