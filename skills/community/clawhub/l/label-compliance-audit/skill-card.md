## Description:

智能审核食品包装标签的合规性，支持图片/PDF设计稿；当用户需要审核标签强制性标识、营养标签规范性、声称用语合规性或格式要求时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudyxuq](https://clawhub.ai/user/cloudyxuq)

### License/Terms of Use:

MIT-0

## Use Case:

External label, product, and compliance reviewers use this skill to review Chinese food packaging label drafts from images or PDFs. It extracts label content, checks GB7718 and GB28050 requirements, claim wording, allergen and format issues, and returns nonconformities with risk levels and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded packaging drafts may contain confidential product designs or label information.

Mitigation: Avoid uploading confidential designs unless the user is comfortable having the agent process them.

Risk: Food-label compliance findings may be incomplete or incorrect when source images are hard to read or regulatory judgment is required.

Mitigation: Have a qualified compliance reviewer verify the report before using it for commercial or regulatory decisions.

## Reference(s):

- [GB7718 prepackaged food label reference](references/gb7718-standard.md)
- [GB28050 nutrition label reference](references/gb28050-standard.md)
- [Claims wording compliance guideline](references/claims-guideline.md)
- [Audit checklist template](assets/audit-checklist.md)
- [ClawHub skill page](https://clawhub.ai/cloudyxuq/skills/label-compliance-audit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include checklist-style pass/fail/N/A entries, nonconformity summaries, risk levels, and remediation suggestions.]

## Skill Version(s):

1.0.1 (source: server release evidence, released 2026-04-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
