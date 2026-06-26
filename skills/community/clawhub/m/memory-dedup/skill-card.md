## Description: <br>
Automatically identifies, merges, and cleans duplicate or outdated entries in MEMORY.md to keep agent memory concise and organized. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidadong2359](https://clawhub.ai/user/weidadong2359) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect MEMORY.md, preview duplicate memory cleanup, and optionally rewrite the file with merged entries and a backup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill rewrites persistent agent memory with weaker safeguards than it claims. <br>
Mitigation: Run the dry-run command first, keep an independent backup, and manually review proposed changes before allowing writes. <br>
Risk: Scheduled automatic cleanup can modify MEMORY.md without immediate human review. <br>
Mitigation: Avoid enabling the weekly cron job unless unattended persistent-memory edits are acceptable for the deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/weidadong2359/memory-dedup) <br>
- [Artifact Skill Documentation](artifact/SKILL.md) <br>
- [Artifact Package Metadata](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and plain-text execution reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update MEMORY.md and create a local memory backup when run outside dry-run mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
