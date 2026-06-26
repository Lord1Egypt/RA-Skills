## Description: <br>
Memory Evolver helps agents diagnose local OpenClaw memory files, generate optimization plans, and maintain an optimization history for a three-layer memory workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horizoncove](https://clawhub.ai/user/horizoncove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect and improve a local OpenClaw memory workspace by checking MEMORY.md, PROJECTS.md, daily logs, and knowledge graph state, then recording optimization cycles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and writes local OpenClaw memory and project files. <br>
Mitigation: Back up important memory files before running it and review generated optimization log entries before relying on them. <br>
Risk: The packaged script uses a hard-coded Administrator workspace path. <br>
Mitigation: Confirm or adjust the workspace path for the target environment before execution. <br>
Risk: The daily cron schedule can repeatedly modify local optimization history. <br>
Mitigation: Enable scheduled execution only deliberately and monitor the first runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/horizoncove/memory-evolver) <br>
- [Publisher profile](https://clawhub.ai/user/horizoncove) <br>
- [Packaged skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-oriented console text and optimization log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes an optimization log in the configured local OpenClaw memory directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
