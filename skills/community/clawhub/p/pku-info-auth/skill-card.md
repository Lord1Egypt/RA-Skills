## Description: <br>
PKU unified credential management CLI (统一凭据管理) for authenticating with PKU services, managing stored credentials, and checking session status across related service CLIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjsoj](https://clawhub.ai/user/wjsoj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to set up and check PKU authentication without exposing passwords to the agent. It guides secure credential storage through the OS keyring and helps agents trigger login flows for PKU services when sessions are missing or expired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles authentication setup for PKU services and may involve sensitive credentials or SMS codes. <br>
Mitigation: Use `info-auth store` with the OS keyring, provide SMS codes only for the immediate login command, and avoid storing passwords in shell profiles, logs, or long-lived environment variables. <br>
Risk: Environment-variable credentials can be exposed through process environments, shell history, or logs. <br>
Mitigation: Prefer OS keyring-backed credentials and reserve `PKU_USERNAME`, `PKU_PASSWORD`, and `PKU_SMS_CODE` for short-lived automation where exposure is controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wjsoj/pku-info-auth) <br>
- [Publisher profile](https://clawhub.ai/user/wjsoj) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance should avoid exposing passwords and should prefer OS keyring storage over long-lived environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
