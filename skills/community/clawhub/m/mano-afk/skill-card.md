## Description: <br>
Autonomous full-cycle app builder - PRD, architecture, code, deployment, testing, and bug fixing from a natural language description. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanningwang](https://clawhub.ai/user/hanningwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill when they explicitly want an agent to autonomously plan, build, deploy, test, and fix an application from a natural language request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can autonomously create, run, deploy, and test local applications. <br>
Mitigation: Use disposable project directories and review generated files, commands, and reports before relying on the result. <br>
Risk: Generated builds or tests may touch sensitive data or production-like services if pointed at them. <br>
Mitigation: Avoid production databases and real customer data during builds and tests. <br>
Risk: LLM/API app builds may require credentials or API-key environment variables. <br>
Mitigation: Review required environment variables before running and provide only credentials appropriate for the test project. <br>
Risk: Cloud E2E mode may send screenshots and task descriptions to cloud VLA providers. <br>
Mitigation: Use cloud E2E only after explicit configuration, or choose local mode or skip E2E when project data should remain local. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanningwang/mano-afk) <br>
- [Publisher profile](https://clawhub.ai/user/hanningwang) <br>
- [Skill homepage](https://github.com/Mininglamp-AI/mano-afk) <br>
- [Build pipeline reference](references/build-pipeline.md) <br>
- [Project structure reference](references/project-structure.md) <br>
- [PRD template](references/prd-template.md) <br>
- [README template](references/readme-template.md) <br>
- [Report template](references/report-template.md) <br>
- [Build rules](references/rules.md) <br>
- [User preferences](references/preferences.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown prose with generated project files, shell commands, reports, and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update project files, deployment scripts, test reports, rules, and preferences within the skill workflow.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
