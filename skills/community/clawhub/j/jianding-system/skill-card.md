## Description:

收藏雅集网在线鉴定 helps an agent guide users through antique and collectible appraisal requests, including photo collection, order submission, payment QR generation, and result lookup for the 收藏雅集网 service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fozu2024](https://clawhub.ai/user/fozu2024)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit paid image-based antique appraisal orders through 收藏雅集网, receive payment instructions, and retrieve appraisal results. The skill is intended for appraisal workflow assistance, not legal certification or guaranteed valuation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends collectible photos, descriptions, phone numbers, SMS or WeChat login data, and order details to an external paid appraisal service.

Mitigation: Use the skill only when the user consents to the 收藏雅集网 service flow, explain the paid third-party nature of the service, and avoid submitting unnecessary personal data.

Risk: The fallback script stores a login token locally at ~/.jianding_token.

Mitigation: Use a virtual environment or isolated account where practical and delete ~/.jianding_token when the appraisal workflow is complete.

Risk: Platform statistics and background claims in the bundled reference are static and may become outdated.

Mitigation: Describe those claims as historical release-time information and direct users to the service site for current details.

Risk: Image-based online appraisal results may be unsuitable as legal proof or a definitive market transaction price.

Mitigation: Present results as service-provided appraisal guidance and recommend appropriate professional or legal channels for high-stakes decisions.

## Reference(s):

- [收藏雅集网 service site](https://jiand.shoucangyaji.com/)
- [ClawHub skill page](https://clawhub.ai/fozu2024/skills/jianding-system)
- [Publisher profile](https://clawhub.ai/user/fozu2024)
- [Platform background reference](references/about.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, text, code, files]

**Output Format:** [Markdown-style guidance with shell commands and local QR image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate a local payment QR image and store a local login token at ~/.jianding_token.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
