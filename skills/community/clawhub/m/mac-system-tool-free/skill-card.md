## Description: <br>
Mac 系统工具 helps personal macOS users inspect system, process, disk, battery, network, screenshot, clipboard, and Finder state and perform basic local controls with confirmation for destructive actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to inspect and control a local macOS system, including system status checks, volume and brightness changes, network diagnostics, screenshots, clipboard operations, Finder actions, and confirmed destructive operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-impact local commands can stop processes or remove files if the target is wrong. <br>
Mitigation: Require explicit user confirmation of process IDs, file paths, and destructive intent before running kill, shutdown, restart, or trash-emptying commands. <br>
Risk: Screenshot and clipboard operations may expose sensitive local data. <br>
Mitigation: Avoid these commands around secrets or private windows, and clear or replace sensitive clipboard contents after use. <br>
Risk: The artifact includes an unrelated data-analysis trigger that can route non-macOS requests to this skill. <br>
Mitigation: Use the skill only for macOS system-control requests and reject data analysis, reporting, statistics, or visualization tasks as out of scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/mac-system-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command output summaries, execution logs, and error details when actions are performed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; SKILL.md frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
