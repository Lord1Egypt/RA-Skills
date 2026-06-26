## Description: <br>
Cortex provides local-first agent memory with file import, fact extraction, hybrid BM25 and semantic search, confidence tracking, MCP tools, and SQLite storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hurttlocker](https://clawhub.ai/user/hurttlocker) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use Cortex to preserve and search persistent memory across OpenClaw sessions, especially for multi-agent setups, large knowledge bases, and workflows where context compaction loses important details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script downloads and executes an external Cortex binary. <br>
Mitigation: Use a pinned and verified Cortex release, review the upstream source or binary, and run setup only in environments where this persistent memory tool is intended. <br>
Risk: Cortex can centralize sensitive imported files, facts, and connector data in a local database. <br>
Mitigation: Start with a small non-sensitive folder, review provider scopes before connector sync, and avoid all-provider sync until each data source is understood. <br>
Risk: Scheduled sync and shell startup modifications can persist beyond the initial setup session. <br>
Mitigation: Do not enable scheduled sync until the disable path is known, and review shell startup file changes after setup. <br>
Risk: The reimport workflow can remove the existing Cortex database. <br>
Mitigation: Back up the Cortex database before using reimport or any full reimport workflow. <br>


## Reference(s): <br>
- [Cortex skill page](https://clawhub.ai/hurttlocker/hurttlocker-cortex) <br>
- [Publisher profile](https://clawhub.ai/user/hurttlocker) <br>
- [Cortex homepage](https://github.com/hurttlocker/cortex) <br>
- [Cortex releases](https://github.com/hurttlocker/cortex/releases) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Wrapper commands may emit JSON from the Cortex CLI for search, stats, stale facts, and conflicts.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
