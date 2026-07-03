## Description: <br>
B2B lead prospecting and outreach via the Okki Go platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okki-op](https://clawhub.ai/user/okki-op) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and sales teams use this skill to search for B2B prospect companies, find decision-maker contact emails, draft or send outbound outreach, check delivery status, and view credit or quota balance through Okki Go. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use real credits for company unlocks and contact searches, and can send outbound email. <br>
Mitigation: Verify credit prompts before paid unlocks or contact searches, and confirm recipients plus content before any email send. <br>
Risk: The skill handles contact data, outbound email content, and saved local lead or status files. <br>
Mitigation: Protect saved files or delete them when no longer needed, and use compact outputs that avoid exposing raw identifiers and unnecessary detail. <br>
Risk: Installer and update notification scripts can configure local credentials or recurring update checks. <br>
Mitigation: Review installer commands, approve API-key storage deliberately, and enable recurring update notifications only when wanted. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/okki-op/skills/okki-go) <br>
- [Publisher profile](https://clawhub.ai/user/okki-op) <br>
- [Okki Go](https://go.okki.ai) <br>
- [Okki Go pricing](https://go.okki.ai/pricing) <br>
- [Authentication and API Key Setup](artifact/references/authentication.md) <br>
- [Paid Actions](artifact/references/paid-actions.md) <br>
- [Context Firewall](artifact/references/context-firewall.md) <br>
- [Output Contracts](artifact/references/output-contracts.md) <br>
- [API Reference](artifact/references/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with script-rendered tables, compact status summaries, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save raw lead, contact, email status, or unlock detail files while keeping normal responses compact and user-facing.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
