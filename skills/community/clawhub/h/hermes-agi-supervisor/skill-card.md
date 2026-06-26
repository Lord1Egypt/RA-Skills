## Description: <br>
Hermes AGI Supervisor turns vague AGI instructions into measurable subtasks with scoring, verification, and rewrite guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mengxiangshu666](https://clawhub.ai/user/mengxiangshu666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert broad task requests into concrete subtasks, completion criteria, scoring rules, and rewrite prompts for iterative supervision. It supports task planning in business, workplace, content creation, and learning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task prompts are stored locally under ~/.hermes and may contain sensitive wording. <br>
Mitigation: Avoid entering secrets, credentials, sensitive business plans, or personal data unless local retention is acceptable; delete ~/.hermes when the history is no longer needed. <br>
Risk: The scorer can modify the JSON task file path provided to it. <br>
Mitigation: Use task files created by this skill and review file paths before running the score command. <br>
Risk: Generated task decomposition and scoring guidance can be incomplete or misleading for high-impact decisions. <br>
Mitigation: Review decomposed tasks, completion criteria, and scoring outcomes before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mengxiangshu666/hermes-agi-supervisor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON task or score files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local helper scripts may create or update JSON files under ~/.hermes.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
