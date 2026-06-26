## Description: <br>
Build and operate autonomous AI businesses using hierarchical agent systems with CEO, Manager, Supervisor, and Worker agents, daily tracking, auto-optimization, and self-healing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miknasbh-stack](https://clawhub.ai/user/miknasbh-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Founders, operators, and agent builders use this skill to design folder-based AI company structures, spawn CEO, manager, supervisor, and worker agents, and set up daily reporting for business operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent autonomous business agents and scheduled reporting may operate beyond intended boundaries. <br>
Mitigation: Inspect generated cron entries before enabling them and keep approval gates for outreach, sales, HR, accounting, onboarding, and actions that change real business data or contact real people. <br>
Risk: Business reports and agent session history may contain sensitive operational information. <br>
Mitigation: Avoid placing credentials or confidential records in agent sessions, and control access to generated reports and business folders. <br>
Risk: Setup scripts create local business folders, reporting scripts, and cron jobs. <br>
Mitigation: Review the generated files and scheduled jobs before relying on them, and remove or update the crontab entries when the business workflow changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miknasbh-stack/miknas-ai-business-hierarchies) <br>
- [README](artifact/README.md) <br>
- [Business template](artifact/assets/business-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes folder structures, agent role prompts, setup commands, reporting scripts, and scheduled report configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
