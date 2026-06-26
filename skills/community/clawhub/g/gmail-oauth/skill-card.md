## Description: <br>
Set up Gmail API access via gog CLI with manual OAuth flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kai-jar](https://clawhub.ai/user/kai-jar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure Gmail API OAuth access for the gog CLI on local or headless systems, renew expired tokens, and troubleshoot Gmail authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles long-lived Gmail OAuth credentials that can provide broad mailbox access. <br>
Mitigation: Protect the OAuth client secret and refresh token, use the narrowest Gmail scope that meets the need, and revoke access from the Google account when the integration is no longer needed. <br>
Risk: Persisting GOG_KEYRING_PASSWORD in a shell startup file may expose the keyring password to other local processes or backups. <br>
Mitigation: Prefer an interactive prompt or a more protected secret store instead of placing the keyring password in .bashrc. <br>
Risk: The flow imports tokens into the gog CLI credential store, so compromise or misuse of that CLI can affect Gmail access. <br>
Mitigation: Install only when intentionally setting up Gmail access for gog and when the gog CLI is trusted in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kai-jar/gmail-oauth) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>
- [Gmail modify OAuth scope](https://www.googleapis.com/auth/gmail.modify) <br>
- [Google OAuth token endpoint](https://oauth2.googleapis.com/token) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and an executable shell helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides users through an interactive or command-line OAuth authorization code flow for gog.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
