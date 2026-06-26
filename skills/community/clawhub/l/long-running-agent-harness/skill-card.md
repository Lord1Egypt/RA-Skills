## Description: <br>
Long-running agent workflow automation that initializes project scaffolding, manages feature lists, tracks progress across sessions, and orchestrates coding agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenkangwei](https://clawhub.ai/user/wenkangwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to structure long-running coding work into initialized project state, feature tracking, per-session progress logs, and handoffs for coding agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The harness can modify a project directory, create tracking files, run local scripts, install dependencies, and affect git history. <br>
Mitigation: Use it in a clean clone or branch, inspect generated scripts before running them, and review git status and diffs before committing changes. <br>
Risk: Reset or recovery guidance can discard tracked local changes when used intentionally. <br>
Mitigation: Confirm that work is backed up or committed before using reset-style commands such as git checkout . or harness reset. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/wenkangwei/long-running-agent-harness) <br>
- [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown prompts, JSON configuration, shell scripts, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates project-local tracking files and may guide git commits during harness workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
