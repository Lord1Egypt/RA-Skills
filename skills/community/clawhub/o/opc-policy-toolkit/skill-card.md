## Description: <br>
政策申报全流程工具包，为OPC导师和项目负责人提供政策获取、申报管理和匹配分析的流程、模板与方法。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golngod](https://clawhub.ai/user/golngod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OPC mentors, project leads, and business operators use this skill to structure policy discovery, company eligibility checks, application material planning, department coordination, and policy-project matching for grant, tax, qualification, talent, and innovation program applications. <br>

### Deployment Geography for Use: <br>
Global; the provided policy examples and application workflows are focused on Chinese government policy programs. <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive identity, payroll, banking, credit, employee, and business records during policy-application work. <br>
Mitigation: Redact unnecessary sensitive fields, restrict where generated Markdown and JSON outputs are stored or shared, and define deletion expectations before use. <br>
Risk: Agent actions such as web searches, file creation, or handoff to other skills may expose sensitive policy-application context if run without review. <br>
Mitigation: Require explicit approval before web searches, file creation, or inter-skill handoff, and review generated outputs before deployment or submission. <br>
Risk: Policy recommendations, eligibility checks, deadlines, and material lists may be incomplete or outdated for a specific jurisdiction or program. <br>
Mitigation: Verify application requirements and deadlines against the relevant official policy source before relying on generated guidance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/golngod/opc-policy-toolkit) <br>
- [Coze platform](https://coze.cn) <br>
- [OPC platform](https://opc.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with checklists, tables, scoring models, timelines, and handoff-oriented JSON descriptions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include policy ledgers, matching reports, application material lists, timelines, and execution reports for review before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
