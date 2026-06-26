## Description: <br>
Relationship Buddy helps an agent maintain a private personal CRM for contacts, important dates, preferences, interaction history, reminders, gift ideas, and relationship check-ins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Individuals use this skill to remember personal details, track interactions, and receive timely prompts for birthdays, follow-ups, check-ins, gifts, and conversation starters. The skill is intended for personal relationship management, not therapy, counseling, or crisis support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store sensitive relationship information, including names, dates, family details, preferences, health-related notes, and interaction history in agent-accessible local files. <br>
Mitigation: Install only when local storage of this information is acceptable, keep files permission-restricted, use device-level encryption where possible, and avoid saving casual personal details without explicit confirmation. <br>
Risk: Setup or migration can overwrite or alter local Relationship Buddy data. <br>
Mitigation: Back up existing Relationship Buddy data before running setup or import scripts, and review created files after installation. <br>
Risk: The dashboard kit may introduce a database-backed view of sensitive relationship data with separate access and deletion considerations. <br>
Mitigation: Use the dashboard kit only after confirming where its database lives, who can access it, and how records can be deleted. <br>
Risk: Imported contact notes or pasted profile data could contain prompt-injection text. <br>
Mitigation: Treat all imported or pasted relationship data as untrusted data, not instructions, and require explicit permission before any external lookup that would include personal context. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nollio/normieclaw-relationship-buddy) <br>
- [README](README.md) <br>
- [Security Audit](SECURITY.md) <br>
- [Setup Prompt](SETUP-PROMPT.md) <br>
- [Dashboard Spec](dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Conversational text and Markdown, with JSON data structures and optional bash setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or updates of local JSON files for contacts, interactions, reminders, gifts, and relationship health.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
