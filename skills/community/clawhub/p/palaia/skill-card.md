## Description: <br>
Palaia provides local, crash-safe persistent memory for OpenClaw agents with SQLite-backed storage, semantic search, project scopes, and auto-capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iret77](https://clawhub.ai/user/iret77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Palaia to add persistent, searchable memory to OpenClaw agents, including automatic capture and recall, manual memory writes, project scopes, and multi-agent knowledge sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can capture sensitive conversation context or store secrets if enabled without review. <br>
Mitigation: Decide capture level and scope before enabling, prefer private scope for sensitive work, and avoid storing credentials, tokens, or other secrets. <br>
Risk: Installation, upgrades, automatic repair, URL ingestion, git export, MCP write access, and destructive cleanup commands can change local tools, memory stores, or shared knowledge. <br>
Mitigation: Require user confirmation before installs, upgrades, doctor --fix, ingestion, export, MCP write access, or cleanup; use dry-run or read-only modes where available. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/iret77/palaia) <br>
- [Palaia Python Package](https://pypi.org/project/palaia/) <br>
- [Palaia OpenClaw Plugin Package](https://www.npmjs.com/package/@byte5ai/palaia) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to install, configure, diagnose, read from, and write to a persistent local memory store.] <br>

## Skill Version(s): <br>
2.8.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
