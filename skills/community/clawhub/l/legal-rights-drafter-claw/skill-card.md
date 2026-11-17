## Description:

法律维权草拟虾。识别违约行为并自动起草维权通知函。当用户提到违约、维权、发函、催告、索赔、侵权、律师函、催款函、警告函、追责等场景时使用。输入可以是自然语言描述或结构化数据（Excel/CSV），输出标准化法律函件（Markdown/PDF/Word）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

External users, business teams, and legal reviewers use this skill to turn Chinese dispute facts into draft rights-enforcement letters, demand letters, breach notices, IP warning letters, and related documents for review before sending.

### Deployment Geography for Use:

China (PRC-law-oriented content)

## Known Risks and Mitigations:

Risk: Legal-letter drafts may contain incorrect facts, amounts, dates, contract clauses, legal citations, or jurisdictional assumptions.

Mitigation: Verify all user-supplied facts and legal references, and have legal counsel or a qualified reviewer approve any letter before it is sent.

Risk: PDF or DOCX conversion can process unsafe Markdown content such as embedded HTML, images, stylesheets, or external links.

Mitigation: Convert only trusted or sanitized Markdown and review generated documents before distribution.

## Reference(s):

- [Legal Clauses](references/legal-clauses.md)
- [Letter Templates](references/letter-templates.md)
- [Case References](references/case-references.md)
- [ClawHub Skill Page](https://clawhub.ai/tujinsama/skills/legal-rights-drafter-claw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown legal-letter drafts with optional shell command snippets for PDF or DOCX conversion]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create PDF or DOCX files when the user requests conversion and required local tools are installed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
