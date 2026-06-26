## Description: <br>
Use passlane, a Keepass-backed password manager and authenticator CLI, to retrieve credentials, payment cards, secure notes, and TOTP codes for automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[passlane](https://clawhub.ai/user/passlane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to script authenticated workflows, fetch stored secrets from a user-managed passlane vault, generate just-in-time TOTP codes, and audit local credential entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Passlane commands can print passwords, payment card details, secure notes, or TOTP codes to stdout. <br>
Mitigation: Pipe secrets directly to the consuming command, avoid writing them to chat, logs, or committed files, and use narrowly scoped selectors. <br>
Risk: A locked vault can block unattended automation on an interactive prompt. <br>
Mitigation: Stop and ask the user to run the appropriate passlane unlock command instead of attempting to provide a master password. <br>
Risk: Broad regular expressions can match no entries or multiple entries and cause incorrect or failed secret retrieval. <br>
Mitigation: Use anchored patterns for single-secret commands and treat exit code 1 as an actionable failure. <br>
Risk: TOTP codes are short-lived and can expire between retrieval and use. <br>
Mitigation: Fetch TOTP codes just before submission and re-fetch on each retry instead of caching them. <br>


## Reference(s): <br>
- [Passlane ClawHub page](https://clawhub.ai/passlane/passlane) <br>
- [Passlane publisher profile](https://clawhub.ai/user/passlane) <br>
- [passlane automation examples](references/automation-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that retrieve cleartext secrets or short-lived TOTP codes from the user's local vault.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
