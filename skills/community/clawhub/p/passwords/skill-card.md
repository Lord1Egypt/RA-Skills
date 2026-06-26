## Description: <br>
Local credential vault with OS keychain integration, encrypted storage, and session-based access control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to maintain a local encrypted credential vault and guide controlled credential access during agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real credentials through agent workflows. <br>
Mitigation: Require user confirmation for credential use where possible and install only when agent-assisted credential handling is acceptable. <br>
Risk: TOTP secrets or critical accounts stored in the same vault can increase account compromise impact. <br>
Mitigation: Avoid storing TOTP secrets or critical accounts unless the user explicitly accepts the risk, and prefer a dedicated audited password manager for high-value accounts. <br>
Risk: Local vault or OS keychain exposure could reveal credential material. <br>
Mitigation: Protect the vault directory and OS keychain, and keep credential access session-scoped. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/passwords) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration] <br>
**Output Format:** [Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the age binary; release metadata lists linux, darwin, and win32 support.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
