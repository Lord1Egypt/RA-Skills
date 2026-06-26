## Description: <br>
Persistent memory for agents that stores preferences, decisions, facts, and events as a connected knowledge graph recalled by who, what, when, or why. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harshidwasekar](https://clawhub.ai/user/harshidwasekar) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agents use this skill to persist, recall, consolidate, and expire long-term memories about user preferences, project decisions, facts, procedures, and events. It is suited for agent workflows that need structured memory across sessions through an MCP server backed by a local SQLite database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can expose private or sensitive user and project information if inappropriate data is stored. <br>
Mitigation: Use the skill only when long-term memory is intended, avoid saving credentials or highly sensitive personal, health, legal, financial, or HR data unless clearly needed and consented to, and review memories periodically. <br>
Risk: The local SQLite memory database can retain information beyond the original interaction context. <br>
Mitigation: Protect the database file path configured by HYPABASE_DB_PATH and use forget to expire old, low-strength, or entity-specific memories. <br>
Risk: The skill installs and runs through uvx, which may matter in environments with stricter package supply-chain controls. <br>
Mitigation: Pin or verify the uvx package source according to the deployment environment's dependency and provenance requirements. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/harshidwasekar/hypabase-memory) <br>
- [Hypabase homepage](https://hypabase.app) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and MCP tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides setup guidance for uvx and HYPABASE_DB_PATH plus examples for remember, recall, consolidate, and forget.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
