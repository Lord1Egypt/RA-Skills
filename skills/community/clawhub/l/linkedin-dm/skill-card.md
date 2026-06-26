## Description: <br>
Send personalized LinkedIn direct messages to existing first-degree connections through browser automation, using an approved pitch and per-recipient relationship hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[10Madh](https://clawhub.ai/user/10Madh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, founder, recruiting, and community operators use this skill to prepare and send reviewed LinkedIn outreach to existing first-degree connections. It supports lead nurturing, event follow-up, reconnection campaigns, and announcements while tracking outreach status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a logged-in LinkedIn session to inspect profiles and send outreach. <br>
Mitigation: Review the recipient list and every generated message before sending, and stop immediately if LinkedIn shows account or rate warnings. <br>
Risk: Outreach logs can contain contact details, relationship hooks, and full message bodies. <br>
Mitigation: Use a private Google Sheet or the local sidecar only when appropriate, and avoid storing sensitive personal or commercial information unnecessarily. <br>
Risk: The workflow includes automation-detection avoidance guidance that can put the LinkedIn account at risk. <br>
Mitigation: Use conservative batch sizes, keep human oversight in the loop, and ensure outreach practices comply with the account holder's policies and platform obligations. <br>


## Reference(s): <br>
- [Browser Automation Workflow](references/browser-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with message text, browser automation steps, shell commands, and optional JSON progress records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces personalized opener and pitch text, CRM tracking rows, and status values for each recipient.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
