## Description:

轻排车间日报（广州轻排信息科技有限公司官方技能）- 汇总今天的开工、完工、报工量、异常与逾期情况，生成一段可直接发群的日报。当用户提到：今天生产怎么样、今天做了多少、车间日报、今天报了多少工、有哪些异常、哪些单逾期、帮我写个日报 时使用。不触发：月度经营分析、财务报表、人员考勤。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengjinfa](https://clawhub.ai/user/zhengjinfa)

### License/Terms of Use:

MIT-0

## Use Case:

生产主管和车间管理人员可用此技能汇总当天的在制、开工、完工、报工、逾期和异常情况，并生成可直接发到工作群的日报。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial and did not fully inspect assets/icon.png; the scan does not establish that the icon is safe.

Mitigation: Review the icon asset before installing the skill.

Risk: A daily report can mislead readers if planned starts are presented as completed starts, report quantities are treated as whole-factory output, or incidents are left unclassified.

Mitigation: Follow the skill's counting rules, retain source precision, classify incidents, and identify overdue work orders from the system records.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhengjinfa/skills/pmclite-daily-report)
- [MRP-PMC official site](https://www.pmclite.com)
- [MRP-PMC install and MCP guide](artifact/references/install.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese plain-text or Markdown daily production report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed report structure, preserves reported precision, and lists up to three prioritized items needing attention.]

## Skill Version(s):

1.0.0 (source: skill metadata and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
