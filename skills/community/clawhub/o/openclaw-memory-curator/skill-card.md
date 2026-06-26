## Description: <br>
Organize, deduplicate, summarize, and compress OpenClaw or Clawd memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1217047020](https://clawhub.ai/user/1217047020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users who maintain OpenClaw or Clawd workspaces use this skill to back up, inspect, deduplicate, summarize, and compress local memory files into concise long-term notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite local memory notes and compressed summaries may omit details. <br>
Mitigation: Confirm the target workspace, require the backup step before changes, review proposed edits, run validation, and compare before-and-after counts. <br>
Risk: Memory files may contain sensitive or stale information. <br>
Mitigation: Keep only durable operational context and omit private data, expired tokens, one-off outputs, and sensitive strings unless the user explicitly needs them retained. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1217047020/openclaw-memory-curator) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON helper-script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update MEMORY.md, compressed memory notes, and memory-backups snapshots after user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
