## Description: <br>
Challenges the user for a secret word before allowing access to sensitive files or system commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cenralsolution](https://clawhub.ai/user/Cenralsolution) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to add a secret-word challenge before sensitive file access, system commands, credential handling, deletions, or similar protected actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is an agent workflow guard and does not provide real operating-system MFA or filesystem access control. <br>
Mitigation: Use it only as a supplemental agent workflow check, review sensitive actions before execution, and do not rely on it as the sole security boundary. <br>
Risk: Password-like material and audit logs are stored under ~/.openclaw and may be readable depending on local permissions. <br>
Mitigation: Use unique high-entropy secret and reset words, avoid reusing account passwords, and protect or review local file permissions for the vault and audit log. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Cenralsolution/mfa-word) <br>
- [Publisher profile](https://clawhub.ai/user/Cenralsolution) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, configuration] <br>
**Output Format:** [Text responses and JSON-like tool status objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns access decisions, setup/reset confirmations, and challenge guidance for protected actions.] <br>

## Skill Version(s): <br>
1.1.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
