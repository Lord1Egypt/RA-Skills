## Description: <br>
Synchronizes and manages multi-channel conversation memories across Feishu, WeChat, Telegram, voice records, and OpenClaw/Hermes stores with MCP access, monitoring, deduplication, and cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lewistouchtech](https://clawhub.ai/user/lewistouchtech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to collect, sync, search, validate, deduplicate, monitor, and maintain personal or workspace memory data across messaging channels and local agent memory stores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and duplicates private conversation and memory data across channels and local stores. <br>
Mitigation: Review exactly which channels, folders, and databases are synced before enabling, and restrict access to the local workspace and memory directories. <br>
Risk: Configured LLM and channel credentials may be used during validation, arbitration, or sync workflows. <br>
Mitigation: Keep API keys in environment variables or a secrets manager, avoid committing keys in configuration files, and scope credentials to the minimum required permissions. <br>
Risk: Cleanup, deduplication, archiving, and memory-delete behavior can remove or rewrite memory records. <br>
Mitigation: Back up Hermes and OpenClaw memory stores, test cleanup on a copy first, and avoid automatic cron cleanup until retention and deletion rules are reviewed. <br>
Risk: MCP or service endpoints bound broadly could expose memory operations beyond the intended local agent. <br>
Mitigation: Bind services locally unless remote access is explicitly required, place any remote endpoint behind authentication, and review available MCP tools before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lewistouchtech/memory-plus-sync) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Documentation](artifact/SKILL.md) <br>
- [Skill Manifest](artifact/skill.yaml) <br>
- [Shared Memory System README](artifact/SHARED_MEMORY_SYSTEM_README.md) <br>
- [Test Report 2026-04-07](artifact/TEST_REPORT_2026-04-07.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with Python code, shell commands, YAML configuration, and JSON status data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May operate on local memory databases, channel sync folders, API-backed model settings, and MCP tool responses.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and artifact/skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
