## Description: <br>
Manage go-to-market activities including contacts, opportunities, pipeline stages, reminders, and signal crawling through a command-line interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, founders, and GTM operators use this skill to track contacts, opportunities, reminders, pipeline state, and prospecting signals for founder-led business development workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill can access live CRM data through Doppler and HubSpot. <br>
Mitigation: Review and gate HubSpot synchronization before use, and grant CRM credentials only when that integration is intended. <br>
Risk: The security review reports an embedded Exa API key without clear disclosure. <br>
Mitigation: Remove or rotate the embedded key and configure API credentials through controlled environment or secret-management settings. <br>
Risk: The local SQLite database can contain contact, deal, and interaction history. <br>
Mitigation: Protect the database file with appropriate filesystem access controls and maintain backups according to the user's data-retention policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aronchick/gtm-system) <br>
- [README.md](artifact/README.md) <br>
- [QUICK_START.md](artifact/QUICK_START.md) <br>
- [SETUP_REPORT.md](artifact/SETUP_REPORT.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell command examples and CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may write and read local SQLite GTM data when its CLI is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
