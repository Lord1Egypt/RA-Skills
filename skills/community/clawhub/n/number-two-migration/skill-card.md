## Description: <br>
Migrates the Number Two OpenClaw agent state, including identity files, memory, system rules, skill integrations, workspace state, and environment configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fr33b1rd8979-max](https://clawhub.ai/user/fr33b1rd8979-max) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
OpenClaw users or developers use this skill when they intentionally want to restore the specific Number Two agent identity, memory, operating rules, skill ecosystem, and current workspace state into a new environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes plaintext credentials and API keys. <br>
Mitigation: Treat included credentials as exposed, remove or rotate them before use, and provide replacement secrets through a safer local mechanism. <br>
Risk: The installer can replace or heavily modify an OpenClaw workspace with the packaged agent state. <br>
Mitigation: Back up the workspace first and install only when the intended outcome is to restore this specific Number Two state. <br>
Risk: The restored state includes broad persistent agent-control instructions, automatic triggers, memory persistence, and external posting or API behavior. <br>
Mitigation: Review the restored AGENTS, HEARTBEAT, SOUL, memory, and skill integration files before enabling the restored environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fr33b1rd8979-max/number-two-migration) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [Number Two Complete State Migration Guide](artifact/二号完整状态迁移指南.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell scripts and bundled configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Restores files into an OpenClaw workspace and provides an installation verifier.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact update log) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
