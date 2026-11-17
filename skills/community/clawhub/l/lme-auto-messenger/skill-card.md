## Description:

Helps operators send personalized messages to LME customers based on spreadsheet category status, using Google Workspace data retrieval and Browser Relay-assisted LME operation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aoaibiz](https://clawhub.ai/user/aoaibiz)

### License/Terms of Use:

MIT-0

## Use Case:

External operators who manage LME and LINE Official Account outreach use this skill to read customer category data from a spreadsheet, generate personalized message drafts, and guide delivery through LME. It is most appropriate when recipients, consent, and message content can be reviewed before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer personal data may be exported from spreadsheets into local JSON files.

Mitigation: Restrict spreadsheet ranges to the fields needed for messaging, protect any exported customer file, and delete it immediately after use.

Risk: Automated customer messaging can result in excessive, unintended, or non-consensual outreach.

Mitigation: Use the skill only with customer opt-in, review recipients and generated messages before sending, and avoid broad bulk sends.

Risk: Browser Relay actions occur through a logged-in LME session and can affect real customer conversations.

Mitigation: Confirm the active LME account, target recipient, and final message in the browser before each send.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aoaibiz/skills/lme-auto-messenger)
- [Publisher profile](https://clawhub.ai/user/aoaibiz)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and message templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authenticated gws access, Browser Relay, an active LME login, and operator review before sending customer messages.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
