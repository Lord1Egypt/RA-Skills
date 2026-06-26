## Description: <br>
LINE messaging integration via Chrome extension gateway. Send/read LINE messages, manage contacts, groups, profile, and reactions. Authenticate with QR code login. Provides HMAC-signed API access through the Chrome extension gateway (line-chrome-gw.line-apps.com). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2manslkh](https://clawhub.ai/user/2manslkh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to operate a LINE account through a Chrome extension gateway, including reading and sending messages, managing contacts and groups, reacting to messages, and updating profile or account settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose private LINE messages and persistent authentication tokens. <br>
Mitigation: Use only with trusted, inspected client code, keep LINE tokens and QR or PIN values private, and avoid sharing generated outputs that contain private chat or account data. <br>
Risk: The skill can change contacts, groups, profile, settings, messages, and account state. <br>
Mitigation: Require explicit approval before performing account-changing actions such as sending, unsending, blocking, inviting, leaving, updating settings, or logging out. <br>
Risk: Packaging and safety guidance are incomplete for a high-privilege messaging client. <br>
Mitigation: Review the artifact and referenced client code before installation, then limit use to the minimum LINE account privileges and conversations needed for the task. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include LINE account identifiers, QR login steps, token handling guidance, and API method usage examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
