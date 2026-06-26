## Description: <br>
Pull personal data such as emails and issues, and propose outbound actions such as drafts and replies, through the PersonalDataHub access control gateway with owner-controlled filtering, redaction, and shaping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haojian](https://clawhub.ai/user/haojian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent retrieve authorized personal data from Gmail and GitHub and propose email actions through a PersonalDataHub gateway with owner policy controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can connect an agent to PersonalDataHub with API-key access to personal data. <br>
Mitigation: Install it only when that access is intended, configure hubUrl and apiKey explicitly, and rely on PersonalDataHub owner policies and redaction for data boundaries. <br>
Risk: Credential setup or discovery may create or expose API keys. <br>
Mitigation: Avoid automatic key creation when possible, rotate any key printed in logs, and store credentials outside shared workspaces. <br>
Risk: GitHub access may use the agent's own credentials outside the PersonalDataHub pull tool. <br>
Mitigation: Confirm that direct GitHub access is acceptable in the workspace and limit the agent's GitHub credentials to intended repositories. <br>
Risk: Outbound email actions could be mistaken for completed sends. <br>
Mitigation: Treat draft, send, and reply requests as pending proposals until the owner approves them in PersonalDataHub. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/haojian/personaldatahub) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance, shell commands, configuration] <br>
**Output Format:** [JSON tool responses with Markdown setup guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool calls require a purpose string; outbound email actions are staged for owner approval before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release, target metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
