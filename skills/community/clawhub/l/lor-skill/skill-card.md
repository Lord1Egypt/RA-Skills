## Description: <br>
A modular five-step engineering verification loop that helps agents plan, execute, check, and summarize work for complex coding and planning tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uwe77](https://clawhub.ai/user/uwe77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a structured verification loop to complex coding, architecture, and planning tasks. It is intended to reduce unsupported final answers by requiring planning, execution, result checking, and concise reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist in agent memory and auto-activate on broad complex-task categories. <br>
Mitigation: Prefer explicit /lor invocation when tighter control is needed, and confirm whether persistent memory registration is desired before installation. <br>
Risk: Verification workflows may involve exec, write, or edit operations. <br>
Mitigation: Keep destructive-operation confirmation enabled and allow read-only operations to run automatically only when that matches the workspace policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/uwe77/lor-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/uwe77) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and console-oriented text with verification steps and summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger local setup commands and agent-memory registration during installation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
