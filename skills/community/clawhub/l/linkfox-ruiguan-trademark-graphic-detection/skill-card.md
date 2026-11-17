## Description:

Detects graphic trademarks in product images and searches for visually similar registered trademarks to help assess logo-related trademark risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, brand owners, and agents use this skill to compare product images against registered graphic trademarks across supported regions before listing or reviewing products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local image uploads create public 24-hour image URLs and send images for LinkFox processing.

Mitigation: Use non-confidential product images unless public temporary hosting and third-party processing are acceptable.

Risk: The artifact includes credential onboarding, billing, payment, and order commands.

Mitigation: Run those commands only when intentionally setting up or purchasing LinkFox access, and use a limited API key where possible.

Risk: LINKFOX_* endpoint environment variables can redirect the skill's network requests.

Mitigation: Verify endpoint environment variables before use and remove unexpected overrides.

Risk: The skill can auto-report feedback through a separate Feedback API.

Mitigation: Review the feedback behavior before installation if automatic reporting is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-ruiguan-trademark-graphic-detection)
- [API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses or saved response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trademark checks require a public image URL; large API responses are saved to local JSON files with a concise stdout summary.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
