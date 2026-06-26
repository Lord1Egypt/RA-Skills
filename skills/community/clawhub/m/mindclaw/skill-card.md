## Description: <br>
MindClaw provides persistent memory and a knowledge graph for AI agents, with structured fact curation, search, conflict detection, and OpenClaw sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Blue8x](https://clawhub.ai/user/Blue8x) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use MindClaw to give OpenClaw and MCP-compatible agents durable, searchable memory across sessions, including curated facts, decisions, preferences, timelines, and prompt-ready context blocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable memory may retain sensitive, personal, confidential, or credential-like content from conversations, logs, configs, or imported Markdown. <br>
Mitigation: Avoid auto-capture and Markdown import on unreviewed sensitive sources; review and redact content before storage, then use archive or hard-delete workflows for entries that should not persist. <br>
Risk: Setup and MCP registration can change future agent tooling and workspace behavior. <br>
Mitigation: Review the selected workspace, agent namespace, database path, and MCP target before approving setup or setup_mindclaw. <br>
Risk: Syncing memories into OpenClaw MEMORY.md can make stored memory visible to other OpenClaw workflows. <br>
Mitigation: Treat sync_openclaw as a publishing step; inspect stored memories before syncing and limit workspace access to the intended users and agents. <br>


## Reference(s): <br>
- [MindClaw ClawHub release](https://clawhub.ai/Blue8x/mindclaw) <br>
- [Blue8x publisher profile](https://clawhub.ai/user/Blue8x) <br>
- [Artifact-declared MindClaw source link](https://github.com/Blue8x/MindClaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text responses with CLI commands, MCP tool calls, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or update local SQLite memory stores, OpenClaw MEMORY.md content, and MCP registration/configuration files when the user authorizes those workflows.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata, pyproject.toml, clawhub.yaml, README badge, CHANGELOG released 2026-03-03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
