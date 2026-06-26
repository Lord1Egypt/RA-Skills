## Description: <br>
Set up Gog CLI for Gmail access and authenticate agent mailboxes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stefanferreira](https://clawhub.ai/user/stefanferreira) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Gog CLI, Google Cloud OAuth, and Gmail authentication for agent mailboxes, then verify and troubleshoot mailbox access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gog access grants mailbox permissions for the selected Gmail account and the setup uses sensitive OAuth client JSON and keyring credentials. <br>
Mitigation: Use an account intended for agent access, review Google OAuth permissions, protect the OAuth client JSON and keyring password, and revoke access when it is no longer needed. <br>
Risk: The setup installs Gog system-wide from a release archive. <br>
Mitigation: Verify the Gog release before installing it system-wide. <br>


## Reference(s): <br>
- [Gog CLI](https://gogcli.sh/) <br>
- [Google Cloud OAuth setup](https://console.cloud.google.com/) <br>
- [OpenClaw Gmail Pub/Sub docs](/automation/gmail-pubsub.md) <br>
- [ClawHub skill page](https://clawhub.ai/stefanferreira/gmail-gog-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Gog CLI and Google OAuth credentials; may involve OAuth client JSON and a keyring password.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
