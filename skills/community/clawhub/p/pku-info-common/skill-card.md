## Description: <br>
PKU Info Common guides agents working with the shared info-common crate for IAAA authentication, OTP, session persistence, credential resolution, and QR rendering across PKU CLI tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjsoj](https://clawhub.ai/user/wjsoj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents working on PKU IAAA-based CLI tools use this skill to understand and modify shared authentication, OTP, session storage, credential resolution, and QR-code workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may expose PKU login credentials, SMS codes, sessions, cookies, keyring entries, or campus-card/payment QR codes. <br>
Mitigation: Use it only for explicitly PKU-related tasks and confirm the user is comfortable before allowing an agent to log in, reuse sessions, read keyring entries, set SMS codes, or display payment QR codes. <br>
Risk: Authentication material can be mishandled if passwords are passed through commands or written into project files. <br>
Mitigation: Prefer OS keyring or environment-variable credential resolution and do not pass passwords as CLI arguments or store them in repository files. <br>


## Reference(s): <br>
- [PKU Info Common on ClawHub](https://clawhub.ai/wjsoj/pku-info-common) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference PKU credential, session, keyring, environment variable, and QR-code workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release; SKILL.md frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
