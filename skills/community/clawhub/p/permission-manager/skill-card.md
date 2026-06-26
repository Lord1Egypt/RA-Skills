## Description: <br>
审批权限管理技能 - 快速切换不同审批模式（白名单/完整权限/免审批） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to inspect and switch command approval modes, including allowlist, full access, no-approval, and strict approval settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently weaken or disable OpenClaw command approvals. <br>
Mitigation: Install only when approval-policy management is intended, prefer default or strict mode, and avoid no-approval mode except temporarily in an isolated trusted environment. <br>
Risk: Configuration changes affect ~/.openclaw/openclaw.json and may require a Gateway restart to fully apply. <br>
Mitigation: Back up or manually verify the configuration file before use, then confirm the active approval settings after changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jirboy/permission-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can report current approval mode, propose configuration changes, and provide success or failure messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
