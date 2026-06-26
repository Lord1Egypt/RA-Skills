## Description: <br>
Email, calendar and contacts access via the Nylas API with typed tools for Gmail, Outlook, Exchange, Yahoo, iCloud, and IMAP accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mqasimca](https://clawhub.ai/user/mqasimca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to Nylas-backed email, calendar, and contacts workflows across supported mail providers. It supports account discovery, message lookup and sending, calendar event management, availability checks, and contact lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read sensitive email, calendar, and contact data through accounts connected to the Nylas API key. <br>
Mitigation: Install only after trusting the Nylas plugin package, use the narrowest practical Nylas grants and scopes, and avoid broad multi-account keys when they are not needed. <br>
Risk: The skill can perform real send, attendee change, event update, and deletion actions without documented confirmation guardrails. <br>
Mitigation: Manually confirm email sends, attendee changes, event updates, and deletions before allowing the action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mqasimca/nylas-email-calendar) <br>
- [Nylas Dashboard](https://dashboard-v3.nylas.com) <br>
- [Installation Guide](https://cli.nylas.com/guides/install-openclaw-nylas-plugin) <br>
- [npm Package](https://www.npmjs.com/package/@nylas/openclaw-nylas-plugin) <br>
- [Nylas CLI](https://cli.nylas.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline shell commands and natural-language tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NYLAS_API_KEY and connected Nylas grants; actions may read account data or send, update, and delete account resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
