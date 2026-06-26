## Description: <br>
Access and manage email, calendar, and contacts across multiple providers using the Nylas API for unified communication and scheduling tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qasim-nylas](https://clawhub.ai/user/qasim-nylas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect Nylas-backed mailboxes, calendars, and contacts so an agent can read messages, draft or send email, manage events, check availability, and look up contacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Nylas-connected email, calendars, and contacts, including sending email and changing events. <br>
Mitigation: Install only for intended accounts, prefer narrowly scoped grants or NYLAS_GRANT_ID for a specific account, and require confirmation before sending email or creating, updating, or deleting calendar events. <br>
Risk: A broad Nylas API key may expose multiple connected accounts through auto-discovery. <br>
Mitigation: Use the narrowest practical Nylas grant and configure NYLAS_GRANT_ID when the agent should operate on only one account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qasim-nylas/nylas) <br>
- [Nylas OpenClaw npm package](https://www.npmjs.com/package/@nylas/openclaw-nylas-plugin) <br>
- [Nylas OpenClaw installation guide](https://cli.nylas.com/guides/install-openclaw-nylas-plugin) <br>
- [Nylas CLI](https://cli.nylas.com) <br>
- [Nylas Dashboard](https://dashboard-v3.nylas.com) <br>
- [Nylas US API endpoint](https://api.us.nylas.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and natural-language agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform Nylas API-backed actions after installation and configuration with a Nylas API key.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
