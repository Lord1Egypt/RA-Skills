## Description: <br>
Google Workspace BYOK gives an agent direct OAuth2 access to Google Calendar and Gmail through the user's own Google Cloud project credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyesh](https://clawhub.ai/user/kyesh) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers, employees, and external users can use this skill to connect an agent to their own Google accounts, inspect Gmail messages and attachments, and read calendar availability or events. It is intended for BYOK workflows where users manage the Google Cloud project, OAuth credentials, and authorized accounts themselves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default authorization flow requests full Google Calendar access and Gmail read access. <br>
Mitigation: Use --readonly unless calendar write access is required, and authorize only the Google accounts needed for the task. <br>
Risk: OAuth credentials and account tokens are stored locally under the user's home directory. <br>
Mitigation: Install and run the skill only on a trusted machine, protect the credential and token files, and remove them when no longer needed. <br>
Risk: Downloaded email attachments can contain untrusted content. <br>
Mitigation: Download attachments only from trusted messages and place them in a dedicated temporary directory before inspection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kyesh/google-workspace-byok) <br>
- [Publisher profile](https://clawhub.ai/user/kyesh) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>
- [Google Auth Platform Audience](https://console.cloud.google.com/auth/audience) <br>
- [Google Auth Platform Clients](https://console.cloud.google.com/auth/clients) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files] <br>
**Output Format:** [Markdown instructions with shell commands; scripts return JSON and may write downloaded attachment files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Node.js scripts, Google OAuth2 credentials, and per-account token files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
