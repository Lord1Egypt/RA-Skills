## Description: <br>
AI-powered personal finance management system - track expenses, manage budgets, analyze spending patterns, and get smart financial recommendations <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhenStaff](https://clawhub.ai/user/ZhenStaff) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to record income and expenses, manage budgets, review spending patterns, and generate personal finance summaries through a local CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or modify local personal finance records through an external CLI. <br>
Mitigation: Review the external npm or GitHub CLI before use and require explicit user confirmation before adding transactions, setting budgets, or changing existing records. <br>
Risk: Local JSON files may contain sensitive personal financial data. <br>
Mitigation: Keep the data directory private, choose a secure custom data path when needed, and avoid sharing the stored files externally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZhenStaff/personal-cfo) <br>
- [NPM package](https://www.npmjs.com/package/openclaw-personal-cfo) <br>
- [Project documentation](https://github.com/ZhenRobotics/openclaw-personal-cfo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local JSON finance records through the external CLI after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
