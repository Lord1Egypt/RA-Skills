## Description:

基于私董会、理事会、专家委员会三会治理体系，整合24位跨领域专家智慧，提供从战略决策到执行落地的完整治理支持系统。

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External users, founders, and business operators use this Chinese-language skill to classify governance questions, match them to private-board, executive-board, or expert-committee perspectives, and produce structured decision advice, execution plans, risk prompts, meeting minutes, decision logs, or skill reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic activation can route sensitive governance questions into advisory workflows without enough context.

Mitigation: Require human review before acting on recommendations, especially for high-impact business, legal, finance, HR, crisis, or public-sector topics.

Risk: Government-relations, personnel-evaluation, legal, finance, and crisis recommendations may be incomplete or inappropriate for the user's jurisdiction or organization.

Mitigation: Treat outputs as drafts only and require review by qualified legal, compliance, finance, HR, or public-affairs owners before execution.

Risk: Users may provide unnecessary confidential, personnel, or public-sector information while seeking advice.

Mitigation: Minimize sensitive inputs, redact personal and confidential details where possible, and keep sensitive actions outside automatic workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/opc-three-governance)
- [理事会4位Agent reference](references/lishihui_4agents.md)
- [私董会9位Agent reference](references/sibodahui_9agents.md)
- [专家委员会11位Agent reference](references/zhuanjiaweiyuanhui_11agents.md)
- [Decision log template](assets/templates/decision_log.md)
- [Meeting minutes template](assets/templates/meeting_minutes.md)
- [Skill report template](assets/templates/skill_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown reports, structured recommendations, JSON-like parameter examples, and Python helper code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language outputs may include problem analysis, multi-perspective recommendations, risk prompts, action plans, meeting minutes, decision logs, and governance reports.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter states 4.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
