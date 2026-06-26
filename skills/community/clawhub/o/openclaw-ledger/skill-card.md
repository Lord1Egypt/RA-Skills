## Description: <br>
Openclaw Ledger provides a local tamper-evident audit trail for agent workspaces by recording workspace snapshots in a hash-chained ledger and verifying whether the chain has been altered. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to initialize, record, verify, inspect, and export a local audit ledger for workspace changes during agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ledger exports and local audit records may contain sensitive workspace file paths, hashes, timestamps, and user-provided messages. <br>
Mitigation: Treat exported ledger output as sensitive and avoid running the skill over unrelated private folders. <br>
Risk: Restore and protect workflows can affect local ledger evidence used for preservation or review. <br>
Mitigation: Review restore and protect behavior before using the skill in evidence-preservation workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AtlasPA/openclaw-ledger) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON, files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; runtime output is console text or JSON plus local JSONL and JSON ledger files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and writes local .ledger files in the selected workspace.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
