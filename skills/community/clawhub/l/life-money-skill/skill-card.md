## Description:

帮助用户通过访谈建档和 7 轮分析完成职业变现诊断，并生成可离线查看的 HTML 报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[luojiangyong](https://clawhub.ai/user/luojiangyong)

### License/Terms of Use:

MIT

## Use Case:

External users and employees use this skill inside an agent to turn career materials, interview answers, income goals, and weekly time constraints into a structured career-monetization report and 90-day plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles sensitive résumé, career-history, and salary information and saves derived files locally.

Mitigation: Redact identifiers that are not needed for the analysis, keep generated project files local, and delete the project output directory when it is no longer needed.

Risk: The generated report may include personal career details that are unsuitable for public sharing.

Mitigation: Review the HTML report before sharing or printing it, and remove any sensitive details that are not required by the recipient.

Risk: Career and income recommendations can be uncertain even when no security issue is present.

Mitigation: Use the skill's confirmation gates and report review step to check assumptions before acting on the recommendations.

## Reference(s):

- [Source repository](https://github.com/LuoJiangYong/life-money-skill)
- [ClawHub skill page](https://clawhub.ai/luojiangyong/skills/life-money-skill)
- [Demo report preview](https://luojiangyong.com/life-money-skill/examples/demo/report.html)
- [7 canonical prompts](references/seven-prompts.md)
- [Interview guide](references/interview-guide.md)
- [Analysis specifications](references/analysis-specs.md)
- [Report design system](references/report-design.md)
- [Market data calibration](references/data-calibration.md)
- [Case library index](references/cases/INDEX.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversational guidance plus JSON profile and analysis files, followed by a single-file HTML report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to remain local under a project directory and are validated against bundled schemas before delivery.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
