## Description:

Memory Indexer helps agents persist, index, and search short-term memory with keyword, semantic-vector, and raw-text retrieval, plus backup, compaction, timeline, and important-memory workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallmj](https://clawhub.ai/user/smallmj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add, index, search, summarize, and maintain OpenClaw memory records, including optional semantic search and backup or compaction workflows for session and memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can persistently modify OpenClaw instruction and heartbeat configuration files.

Mitigation: Review the proposed configuration changes before installation and use a manual install path when persistent behavior changes are not desired.

Risk: Compaction workflows can overwrite original memory or session files after indexing selected content.

Mitigation: Create and verify recoverable backups or snapshots before running compaction, and test restore procedures on non-critical data first.

Risk: Remote embedding providers can receive memory text when enabled.

Mitigation: Keep remote providers disabled unless data sharing is approved; prefer local embeddings for private memory.

Risk: The update script can fetch and apply code from the configured git origin.

Mitigation: Run updates only from a trusted origin and review the current code before executing update.sh.

Risk: Bundled backup directories may include memory index data from prior use.

Mitigation: Remove bundled backup data before redistribution or deployment unless its contents have been reviewed and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallmj/skills/memory-indexer)
- [README_EN.md](README_EN.md)
- [README.md](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Command-line text, Markdown memory files, JSON index files, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include persistent local files under the memory indexer data directory and optional OpenClaw configuration changes.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact docs also mention 2.0.0 and setup.py mentions 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
