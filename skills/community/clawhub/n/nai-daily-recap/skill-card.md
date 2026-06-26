## Description: <br>
Generate a daily recap/summary of all agent activity and save it to Obsidian. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to compile an end-of-day summary of agent activity, including requests, research, created files, decisions, and notable items. It writes a dated Obsidian journal entry and records that the recap was completed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read work-session details and optional Discord messages while preparing the recap. <br>
Mitigation: Set clear limits for allowed sources, channels, and dates before use. <br>
Risk: The skill may persist personal data, credentials, or confidential project details into an Obsidian vault. <br>
Mitigation: Require redaction of secrets, personal data, credentials, and confidential details before the journal entry is written. <br>
Risk: A broad daily recap can capture more information than intended. <br>
Mitigation: Review generated entries and keep the recap scope limited to necessary activity summaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/newageinvestments25-byte/nai-daily-recap) <br>
- [Publisher profile](https://clawhub.ai/user/newageinvestments25-byte) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown journal entry with YAML frontmatter] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to vault/daily-recap/YYYY-MM-DD.md and appends an addendum instead of overwriting an existing entry.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
