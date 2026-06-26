## Description: <br>
Run Codex CLI, Claude Code, OpenCode, or Pi Coding Agent via background process for programmatic control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[branexp](https://clawhub.ai/user/branexp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to run coding assistants in background processes, monitor their progress, and coordinate non-interactive implementation or review tasks across project workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages high-power unattended coding-agent workflows that may run with broad repository or shell access. <br>
Mitigation: Use sandboxed modes where possible, run agents in isolated checkouts or containers, and review proposed changes before merging, pushing, or deploying them. <br>
Risk: Prompts, session logs, PR comments, and command arguments may expose sensitive review material or credentials. <br>
Mitigation: Do not pass API keys on the command line, redact prompts and logs before sharing them, and review generated GitHub comments before posting. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/branexp/giga-coding-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for launching and monitoring external coding-agent processes; users must review and adapt commands before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
