## Description:

根据美国、欧洲、日本或韩国专利号获取专利标题、摘要和权利要求，并生成术语一致的中文专利译文及术语对照表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Patent professionals, researchers, and R&D teams can use the skill to retrieve foreign patent text and prepare Chinese translations with consistent terminology for review and reference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key protection and credential destinations warrant review.

Mitigation: Use a limited trial credential in an isolated workspace, avoid sharing production keys in chat, and verify key-storage and destination restrictions before use.

Risk: Cache-file handling and patent-identifier validation warrant review before file access.

Mitigation: Use public patent numbers in an isolated workspace until identifier validation and cache-file handling have been reviewed.

Risk: Requests send information to PatentMax and may incur charges.

Mitigation: Get approval before sending confidential technical details and confirm expected charges before requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ip930/skills/patent-translate)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [PatentMax API reference](artifact/references/api-reference.md)

## Skill Output:

**Output Type(s):** [Markdown, CSV, Text]

**Output Format:** [Chinese patent translation in Markdown and a UTF-8 CSV terminology glossary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Machine-assisted translation for reference; uncertain terminology should be reviewed.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
