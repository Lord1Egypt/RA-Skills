## Description:

为论文查重提供字数与字符数区分、检测产品选择、费用预估和用户确认后的站点引导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zslzxy](https://clawhub.ai/user/zslzxy)

### License/Terms of Use:

MIT-0

## Use Case:

面向学生、研究人员及论文检测服务人员，解释论文检测的计数与计费口径，帮助选择合适产品，并引导用户自行确认网站及提交文件。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured or default checking-site link may direct users to an unintended site.

Mitigation: Confirm the displayed checking-site URL with the user before they visit or upload a paper; do not submit files on their behalf.

Risk: Broad automatic activation may present paper-checking guidance for related counting or plagiarism questions when it is not wanted.

Mitigation: Check the user's intent and explain the difference between local counts and the target site's final billing count before recommending a product.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zslzxy/skills/paper-character-strategy)
- [计数与计费规则](references/counting-and-billing-rules.md)
- [产品选择指南](references/decision-playbook.md)
- [WPS 字数统计教程](references/wps-word-count-tutorial.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis]

**Output Format:** [Markdown text with optional website link and billing calculations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates are provisional; the chosen site's document analysis, product terms and price govern the final charge.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
