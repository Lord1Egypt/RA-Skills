## Description:

整理企业专利的类别、有效状态和权属来源，并估算高新技术企业认定知识产权数量得分。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

面向准备或复审中国高新技术企业认定的企业，梳理名下专利的 I 类、II 类、有效状态及获得方式，并提供知识产权数量得分估算和可用表格。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Company names and search terms are sent to PatentMax, and requests may consume paid credit.

Mitigation: Use public information and set a spending limit before searching.

Risk: The security review flags API-key storage and transmission for review before connecting a paid account.

Mitigation: Do not paste production keys into chat; before connecting an account, ask the publisher to restrict credential destinations and redirects, protect saved keys, and contain cache paths.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ip930/skills/hitech-patent-prep)
- [PatentMax](https://ip930.com)
- [PatentMax API reference](references/api-reference.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, CSV files]

**Output Format:** [Chinese-language Markdown summary and UTF-8 CSV compatible with spreadsheet applications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Patent classifications, ownership and validity summaries, and an estimated quantity score; results require review against current rules and official records.]

## Skill Version(s):

1.0.2 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
