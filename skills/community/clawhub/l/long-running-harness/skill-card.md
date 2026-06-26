## Description: <br>
A long-running agent project workflow framework for creating, managing, and resuming multi-session project work with persistent project files, feature tracking, progress logs, and verification routines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aowind](https://clawhub.ai/user/aowind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project maintainers use this skill to structure long-running agent work across context windows, initialize project tracking files, select and verify one feature at a time, delegate self-contained tasks to subagents, and report progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can guide agents to edit files, run setup scripts, commit changes, spawn subagents, or schedule recurring checks in the selected workspace. <br>
Mitigation: Use the skill in a clearly scoped project directory, review git status and diffs before commits, and enable recurring checks only when explicitly intended. <br>
Risk: Generated setup scripts or dependency files may run project initialization commands. <br>
Mitigation: Review generated init.sh and dependency files before allowing execution. <br>
Risk: Progress and feature tracking files may capture sensitive project details or secrets. <br>
Mitigation: Avoid storing secrets in progress.md, features.json, or related project tracking files. <br>


## Reference(s): <br>
- [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) <br>
- [Feature List Template](references/feature-list-template.md) <br>
- [Init Script Template](references/init-template.md) <br>
- [Progress Log Template](references/progress-log-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project files such as PROJECT.md, progress.md, features.json, and optional init.sh when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
