## Description: <br>
Generate secure random strings, passwords, and cryptographic tokens using OpenSSL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Asleep123](https://clawhub.ai/user/Asleep123) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to generate passwords, API keys, session tokens, and other random secrets with local OpenSSL commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated passwords, API keys, or tokens could be exposed if left in shared logs, screenshots, or chat history. <br>
Mitigation: Generate secrets in a controlled local shell, avoid sharing command output, and move long-lived secrets directly into an approved secret store. <br>
Risk: The commands depend on local OpenSSL availability and user review before execution. <br>
Mitigation: Confirm OpenSSL is installed and review the command parameters before using generated values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Asleep123/openssl) <br>
- [Publisher profile](https://clawhub.ai/user/Asleep123) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands produce base64, hex, URL-safe, alphanumeric, or numeric random strings depending on the selected example.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
