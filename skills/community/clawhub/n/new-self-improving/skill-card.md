## Description: <br>
Log corrections, errors, feature requests, and recurring patterns into structured workspace learning files, then promote stable patterns into tiered memory and OpenClaw workspace files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muhamadbasim](https://clawhub.ai/user/muhamadbasim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to capture corrections, command failures, feature requests, and recurring work patterns into local learning files, then review and promote stable patterns into workspace memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps durable local memory about user preferences, errors, and work patterns. <br>
Mitigation: Install it only in workspaces where durable memory is desired, review .learnings and .self-improving periodically, and avoid storing secrets, health data, or private third-party data. <br>
Risk: Promoted entries can influence future agent behavior through workspace memory files. <br>
Mitigation: Require manual review before promoting entries into AGENTS.md, SOUL.md, TOOLS.md, or MEMORY.md, and use the documented recurrence and review rules before promotion. <br>


## Reference(s): <br>
- [OpenClaw homepage](https://github.com/muhamadbasim/oktoclaw) <br>
- [logging-format.md](references/logging-format.md) <br>
- [promotion-rules.md](references/promotion-rules.md) <br>
- [heartbeat-review.md](references/heartbeat-review.md) <br>
- [workspace-layout.md](references/workspace-layout.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and maintains local workspace learning and memory files when activated.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
