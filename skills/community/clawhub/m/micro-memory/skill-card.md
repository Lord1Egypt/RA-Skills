## Description: <br>
Micro Memory helps agents create, search, tag, link, review, compress, archive, and report on local plaintext memories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[payne-openclaw](https://clawhub.ai/user/payne-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use Micro Memory to maintain a local memory store for notes, reminders, review scheduling, associative links, search, health summaries, compression, archiving, and export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores user memories as plaintext local files. <br>
Mitigation: Avoid storing secrets or sensitive work data, and review stored memory files before sharing or exporting. <br>
Risk: Compression, consolidation, archive, export, delete, and edit behavior can mutate or move memory data. <br>
Mitigation: Back up the store directory before running destructive or full-data actions and review command output after execution. <br>
Risk: Server security evidence reports broad auto-triggers, weak confirmations, an unsafe helper script, and a malformed package manifest. <br>
Mitigation: Review before installing, prefer a version with narrower triggers and stronger confirmations, and verify package metadata before building or running. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/payne-openclaw/micro-memory) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>
- [Validation Plan](artifact/VALIDATION_PLAN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON files, CSV files, shell commands, guidance] <br>
**Output Format:** [CLI text and Markdown, with optional JSON or CSV exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and mutates plaintext local memory files under the skill store directory.] <br>

## Skill Version(s): <br>
4.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
