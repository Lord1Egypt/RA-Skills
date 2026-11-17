## Description:

Provides a Clawdbot semantic memory store that embeds memory text and search queries with Baidu Embedding-V1, persists records in SQLite, and supports tag-filtered retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xqicxx](https://clawhub.ai/user/xqicxx)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to add persistent semantic memory to Clawdbot, storing conversation context, user preferences, and knowledge snippets locally while retrieving related memories with natural-language queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory text and search queries may be sent to Baidu when embedding generation is enabled.

Mitigation: Review the privacy boundary before use, avoid storing sensitive personal, business, health, financial, or secret data unless approved, and use fallback or local-only behavior where required.

Risk: Operational scripts assume root-level Clawdbot paths and can modify files, permissions, symlinks, backups, and restored data.

Mitigation: Inspect scripts before installation, run them first in an unprivileged test environment, replace hard-coded paths, and require confirmation for cleanup, restore, and maintenance actions.

Risk: Persistent SQLite memory files and backups can retain sensitive or stale information.

Mitigation: Apply filesystem permissions, retention rules, backup validation, and deletion processes for data that should not be retained.

Risk: The embedding client is loaded from an absolute local path and may be unavailable or changed outside this release.

Mitigation: Use a pinned and reviewed embedding client package, verify startup checks, and document fallback behavior before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xqicxx/skills/memory-baidu-embedding-db)
- [Publisher Profile](https://clawhub.ai/user/xqicxx)
- [Baidu Qianfan Console](https://console.bce.baidu.com/qianfan/)
- [README](artifact/README.md)
- [API Reference](artifact/API_REFERENCE.md)
- [Security Configuration](artifact/SECURITY_CONFIG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation with Python and shell code blocks; Python methods return booleans, lists of dictionaries, and statistics dictionaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Baidu API credentials from environment variables and stores persistent memory records in a local SQLite database.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
