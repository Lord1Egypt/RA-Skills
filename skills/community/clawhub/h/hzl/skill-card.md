## Description: <br>
Persistent task ledger for agent coordination. Plan multi-step work, checkpoint progress across session boundaries, and coordinate across multiple agents with project pool routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmchow](https://clawhub.ai/user/tmchow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use HZL to plan multi-step work, preserve progress across sessions, and coordinate handoffs or pooled work across multiple agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and relies on an external HZL CLI package. <br>
Mitigation: Install only trusted HZL packages from the documented Homebrew or npm sources and verify the local CLI before use. <br>
Risk: HZL persists task data that may include sensitive project context or secrets if agents record them. <br>
Mitigation: Avoid putting secrets in task titles, descriptions, links, or checkpoints; scope shared projects to the minimum necessary audience. <br>
Risk: Documented force and prune commands can delete HZL data permanently. <br>
Mitigation: Run force or prune deletion commands only after an explicit user request and confirmation that deletion is intended. <br>


## Reference(s): <br>
- [HZL website](https://hzl-tasks.com) <br>
- [HZL project homepage](https://github.com/tmchow/hzl) <br>
- [ClawHub release page](https://clawhub.ai/tmchow/hzl) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing operating guidance for using the hzl CLI; it does not itself create task data unless the agent runs the suggested commands.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
