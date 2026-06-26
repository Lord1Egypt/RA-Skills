## Description: <br>
Medication Channel routes medication-channel messages through a deterministic local tracker for logging taken, missed, extra, and completed medication events with timestamp-grounded confirmations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cdmichaelb](https://clawhub.ai/user/cdmichaelb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operators, and agents use this skill in a dedicated Discord medication channel to log user-reported medication events accurately, avoid fabricated reminder confirmations, and keep source-message timestamps grounded in the configured local timezone. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medication history and Discord identifiers are stored in a local plaintext CSV. <br>
Mitigation: Use a private WORKSPACE with restrictive filesystem permissions, avoid syncing the log to shared backups, and define a retention or deletion process for medication records. <br>
Risk: Incorrect logging or confirmation could misrepresent whether a medication event occurred. <br>
Mitigation: Use the provided tracker or Discord wrapper path, require source message timestamps, and avoid confirming a log unless the script path actually wrote the event. <br>


## Reference(s): <br>
- [Medication Channel Rules](references/CHANNEL_RULES.md) <br>
- [Medication Channel Reference README](references/README.md) <br>
- [Medication Channel on ClawHub](https://clawhub.ai/cdmichaelb/medication-channel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, short text confirmations, and JSON or CSV outputs from local tracker scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local plaintext CSV medication log and deduplication state under $WORKSPACE/data; uses source Discord message metadata and makes no network calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
