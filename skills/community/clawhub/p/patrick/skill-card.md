## Description: <br>
Access Patrick's expertise library for executive decision infrastructure. List, fetch, and manage structured expertise with context variables. Use for executive briefings, decision framing, and strategic analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MCSH](https://clawhub.ai/user/MCSH) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Executives, operators, and supporting agents use this skill to fetch licensed Patrick expertise templates for briefings, decision framing, strategic analysis, and continuity workflows with optional context variables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad company context and operational data access. <br>
Mitigation: Use only explicitly approved, task-specific company data and avoid blanket access to Slack, JIRA, calendars, Git history, or operational files. <br>
Risk: License handling may expose credentials if pasted into chat. <br>
Mitigation: Configure the Patrick license through a local secure path where possible and avoid sharing license tokens in conversation. <br>
Risk: The install flow downloads and runs a third-party CLI and may configure scheduled jobs. <br>
Mitigation: Review the install script, verify the downloaded CLI and checksum, and enable cronjobs only after confirming exactly what they run and what data they can access. <br>


## Reference(s): <br>
- [Patrick homepage](https://patrickbot.io) <br>
- [Patrick skill on ClawHub](https://clawhub.ai/MCSH/patrick) <br>
- [Patrick portal](https://portal.patrickbot.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and CLI-oriented text with optional structured JSON from fetched expertise] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires patrick-cli, a Patrick license, and approved context data for the selected expertise.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
