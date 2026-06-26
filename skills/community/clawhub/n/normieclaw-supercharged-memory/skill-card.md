## Description: <br>
Supercharged Memory gives an agent persistent, searchable workspace memory for capturing, organizing, retrieving, consolidating, and checking user context across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to add long-term local memory to a workspace agent, including session-start recall, daily note capture, QMD search, memory consolidation, and health checks. It is most useful when continuity across conversations is important and the user is prepared to review stored memory content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records, rewrites, and reuses personal or work context by default. <br>
Mitigation: Install it only in workspaces where always-on long-term memory is intended, and regularly review or edit MEMORY.md and the memory directory. <br>
Risk: Stored memories may contain secrets, regulated personal data, or stale context if users do not curate them. <br>
Mitigation: Avoid capturing secrets or regulated personal data, use forget or direct file edits to remove unwanted entries, and run periodic memory health checks and consolidation. <br>
Risk: Optional Vector DB or dashboard sync paths may process or store memory data outside the local workspace. <br>
Mitigation: Enable those options only after reviewing the selected provider, storage location, and data retention behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nollio/normieclaw-supercharged-memory) <br>
- [README](README.md) <br>
- [Security Audit](SECURITY.md) <br>
- [Setup Prompt](SETUP-PROMPT.md) <br>
- [Memory Configuration](config/memory-config.json) <br>
- [Consolidation Rules](config/consolidation-rules.md) <br>
- [Dashboard Spec](dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples, JSON configuration, and local memory file updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and maintains local workspace memory files; optional vector database or dashboard sync can process memory data outside the base local workflow when enabled.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
