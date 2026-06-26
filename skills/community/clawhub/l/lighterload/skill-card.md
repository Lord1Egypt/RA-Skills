## Description: <br>
Proactive relationship and family care assistant that reduces the invisible cognitive labor of managing a household and maintaining important relationships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Devlines](https://clawhub.ai/user/Devlines) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use LighterLoad to onboard their family and social circle, maintain local notes about important people, and receive periodic care nudges for birthdays, milestones, relationships, holidays, parenting, and household planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally maintains local notes about family, friends, household details, and reminders. <br>
Mitigation: Keep stored details minimal and avoid addresses, full birth dates, account details, sensitive medical information, credentials, and other high-risk identifiers. <br>
Risk: Calendar and messaging access could expose private relationship or household context if granted too broadly. <br>
Mitigation: Grant calendar and messaging access narrowly, require user consent for recurring reminders, and review generated email or .ics content before use. <br>
Risk: Local `memory/people/` notes and recurring jobs can outlive the user's need for the skill. <br>
Mitigation: When stopping use, delete `memory/people/` and remove the associated cron job. <br>


## Reference(s): <br>
- [Care Domains](references/care-domains.md) <br>
- [Holidays, School Terms & Leave Optimisation](references/holidays-and-leave.md) <br>
- [The Mental Load - Research Summary](references/mental-load-research.md) <br>
- [Onboarding Flow](references/onboarding-flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, local Markdown notes, and plain-text iCalendar (.ics) content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create recurring reminder configuration and local memory files when the user consents.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
