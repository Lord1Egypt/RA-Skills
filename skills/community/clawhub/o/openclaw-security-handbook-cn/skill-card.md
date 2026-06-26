## Description: <br>
基于 ZAST.AI 安全手册的 OpenClaw 安全审计与加固技能。运行全面安全诊断（内置 audit + 手册补充项），生成结构化报告，提供交互式修复引导，支持定时审计调度。触发场景：安全审计、安全加固、漏洞检查、security audit、hardening、暴露检查。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruijh](https://clawhub.ai/user/ruijh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to audit local OpenClaw security posture, review findings, receive hardening guidance, and optionally configure recurring security checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security audits may expose sensitive local configuration, logs, sessions, memory content, tokens, or credentials in generated reports. <br>
Mitigation: Ask the agent to redact token values and memory contents before presenting or storing reports, and avoid sharing raw audit output outside the trusted environment. <br>
Risk: Remediation guidance can include commands that change file permissions, add cron jobs, uninstall skills, use sudo/chattr, or delete local data. <br>
Mitigation: Require explicit user confirmation before applying fixes, scheduling jobs, uninstalling skills, using elevated privileges, or running delete commands. <br>
Risk: The skill performs local security checks and command recommendations that may be inappropriate for some OpenClaw deployments. <br>
Mitigation: Review each finding against the actual deployment context before applying changes, especially for sandbox, group policy, OAuth, and workspace cleanup decisions. <br>


## Reference(s): <br>
- [OpenClaw Security Checklist](references/checklist.md) <br>
- [OpenClaw Security Fix Commands](references/fix-commands.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ruijh/openclaw-security-handbook-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured security report sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize OpenClaw audit findings, propose remediation commands, and guide scheduling of recurring security audits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
