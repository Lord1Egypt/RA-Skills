## Description:

个人投资决策辅助系统，基于 INVEST 六维决策框架组织持仓管理、决策评分、仓位计算、风控检查、复盘分析和交互式 HTML 可视化报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to structure personal investment decisions, record portfolio data, calculate position sizing, check risk rules, and generate decision or review reports. It is decision support only and does not replace professional financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores local investment records and generates report files.

Mitigation: Install and use it only when local financial record storage and file generation are acceptable for the user or organization.

Risk: Generated reports may include user-provided record text.

Mitigation: Avoid placing untrusted text in investment records before opening generated HTML reports.

Risk: Report writing behavior needs review.

Mitigation: Use simple report filenames until the file-write boundary is fixed.

Risk: Investment outputs can be mistaken for professional financial advice.

Mitigation: Treat all scores, recommendations, and reports as decision support and require the user to make final investment decisions.

## Reference(s):

- [INVEST decision framework reference](references/framework.md)
- [Investment indicators quick reference](references/indicators.md)
- [ClawHub skill page](https://clawhub.ai/bettermen/skills/investment-decision-system)
- [ClawHub publisher profile](https://clawhub.ai/user/bettermen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown and text responses with Python snippets, shell commands, structured calculations, and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local investment records and HTML reports when the user chooses to save decisions, holdings, trades, or reviews.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
