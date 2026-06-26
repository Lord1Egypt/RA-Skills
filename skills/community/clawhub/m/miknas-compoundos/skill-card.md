## Description: <br>
Design, implement, and operate a self-improving AI Operating System for business with 9 components: Strategic Layer, Prioritization Engine, Knowledge Management, Central Ops, Department Agents (ACRA), Projects, Auto-Capture, Communication Layer, and Metrics & Monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miknasbh-stack](https://clawhub.ai/user/miknasbh-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators, founders, and automation builders use this skill to design a self-improving operating system for strategy, prioritization, knowledge management, department agents, projects, learning loops, communication, and metrics. It provides structured guidance and templates for coordinating AI-powered business workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to retain broad business data, which can expose secrets, personal data, or sensitive records if stored in shared memory. <br>
Mitigation: Use least-privilege access, redact secrets and personal data before storage, define retention and deletion rules, and keep finance, HR, legal, and customer records out of shared agent memory unless explicitly approved. <br>
Risk: Autonomous high-impact business actions could affect payments, invoices, tax filings, payroll, public posts, outreach, customer accounts, or production systems. <br>
Mitigation: Require human approval for those actions and review proposed changes before execution. <br>
Risk: Connecting the operating system to real business systems without controls can amplify incorrect or unsafe agent behavior. <br>
Mitigation: Add operational controls before connecting it to production systems and limit each department agent to the access needed for its role. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/miknasbh-stack/miknas-compoundos) <br>
- [Department Agents - ACRA Framework](references/department-agents.md) <br>
- [Knowledge Management Setup](references/knowledge-setup.md) <br>
- [Learning Loop - Auto-Capture & Intelligence](references/learning-loop.md) <br>
- [Metrics & Monitoring - Operating Rhythm](references/metrics-cadence.md) <br>
- [Strategic Layer Template](assets/strategy-template.md) <br>
- [Department Agent Prompt Templates](assets/department-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance and reusable templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only outputs for business operating workflows, department agent prompts, strategic templates, and metrics cadence setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
