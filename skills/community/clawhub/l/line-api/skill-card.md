## Description: <br>
LINE messaging integration via Chrome extension gateway for sending and reading LINE messages, managing contacts, groups, profile, and reactions, and authenticating with QR code login. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2manslkh](https://clawhub.ai/user/2manslkh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation builders use this skill to let an agent operate a LINE account through a Chrome extension gateway, including messaging, contact and group management, profile and settings changes, reactions, and polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad access to read and change a LINE account. <br>
Mitigation: Require explicit approval before reading chats, sending or deleting messages, changing profile/settings, or managing contacts and groups. <br>
Risk: Persistent LINE tokens are stored under ~/.line-client and can grant account access if exposed. <br>
Mitigation: Protect token files as secrets, avoid logging QR/PIN events, and remove or revoke tokens when finished. <br>
Risk: The release relies on external code not packaged for inspection. <br>
Mitigation: Review the referenced repository code before use and install only when account automation is intended. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/2manslkh/line-api) <br>
- [Repository link referenced in skill text](https://github.com/2manslkh/line-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include QR/PIN authentication steps and API method references; account access should require explicit user approval.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
