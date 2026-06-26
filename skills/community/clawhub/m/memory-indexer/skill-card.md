## Description: <br>
Indexes and searches OpenClaw agent memory using keyword extraction, related-memory discovery, timeline views, important-memory markers, cascading keyword/vector/raw-text search, and memory/session backup and compaction workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallmj](https://clawhub.ai/user/smallmj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to make agent memory searchable, traceable, and compact across sessions. It supports adding, syncing, searching, summarizing, backing up, and compacting local memory and session files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release can persistently change OpenClaw behavior and mutate broad local memory or session data. <br>
Mitigation: Review scripts before installation, prefer manual setup, and back up OpenClaw memory and session files before enabling compaction. <br>
Risk: Bundled backup_* directories may contain stale or unnecessary index state. <br>
Mitigation: Delete bundled backup_* directories before installing or running the skill unless they are intentionally needed. <br>
Risk: The update script can auto-update code and OpenClaw configuration. <br>
Mitigation: Avoid update.sh auto-update behavior unless the repository and publisher are trusted; use manual updates when possible. <br>
Risk: Remote embedding providers may send memory text outside the local machine. <br>
Mitigation: Use local embeddings unless the user explicitly accepts sending memory content to a remote provider. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/smallmj/memory-indexer) <br>
- [Publisher profile](https://clawhub.ai/user/smallmj) <br>
- [README_EN.md](artifact/README_EN.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with command examples and local configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local index, backup, snapshot, and OpenClaw configuration files when its scripts are executed.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
