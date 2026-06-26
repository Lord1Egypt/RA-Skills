## Description: <br>
Manage LinkedIn outreach leads from Google Sheets by searching by name, reading live conversation threads, updating status, and sending contextual follow-up messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[10Madh](https://clawhub.ai/user/10Madh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales and outreach operators use this skill to manage LinkedIn follow-ups from a Google Sheets CRM, review live conversation context, draft replies, send approved messages, and keep pipeline status current. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate through a logged-in LinkedIn account and Google Sheets CRM containing outreach and conversation data. <br>
Mitigation: Confirm the LinkedIn account and Sheet ID belong to the user, restrict sheet sharing, and review each recipient and exact message before sending. <br>
Risk: Conversation history and lead status may be logged persistently in the CRM sheet or local fallback log. <br>
Mitigation: Avoid storing unnecessary sensitive content, keep CRM access limited, and remove local plaintext logs after syncing or when they are no longer needed. <br>
Risk: Batch follow-up behavior and anti-detection instructions can encourage unattended or platform-sensitive messaging. <br>
Mitigation: Avoid unattended batch sends, require explicit approval for each send, respect LinkedIn rules, and ignore or remove anti-detection guidance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/10Madh/linkedin-followup) <br>
- [Browser Workflow](references/browser-workflow.md) <br>
- [CRM Sheet Schema](references/sheet-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, CRM update guidance, and message drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can update Google Sheets records and send LinkedIn messages through a logged-in browser session after user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
