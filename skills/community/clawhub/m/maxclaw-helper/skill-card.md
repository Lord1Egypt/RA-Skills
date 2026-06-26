## Description: <br>
Usage guidance and runtime diagnostics for MaxClaw / OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KrisLiu16](https://clawhub.ai/user/KrisLiu16) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and MaxClaw/OpenClaw users use this skill to answer feature, configuration, onboarding, and troubleshooting questions from trusted documentation. It also helps decide when to stop risky operations and escalate unresolved issues to official community support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste tokens, passwords, private configuration values, or sensitive logs while troubleshooting. <br>
Mitigation: Ask users to redact secrets and sensitive logs before using documentation lookup or sharing details for support. <br>
Risk: Troubleshooting guidance could lead to unsafe edits of critical configuration or irreversible operations. <br>
Mitigation: Require explicit user authorization before modifying openclaw.json or other critical configuration, and stop after repeated failures or unresolved documentation gaps. <br>


## Reference(s): <br>
- [MaxClaw Helper on ClawHub](https://clawhub.ai/KrisLiu16/maxclaw-helper) <br>
- [Trusted Sources - MaxClaw Helper](references/trusted-sources.md) <br>
- [Community Support Template](references/community-template.md) <br>
- [OpenClaw Official Docs](https://docs.openclaw.ai/) <br>
- [OpenClaw CLI Docs](https://docs.openclaw.ai/cli) <br>
- [OpenClaw Gateway Docs](https://docs.openclaw.ai/gateway) <br>
- [OpenClaw Channels Docs](https://docs.openclaw.ai/channels) <br>
- [OpenClaw Skills Docs](https://docs.openclaw.ai/skills) <br>
- [OpenClaw Cron Docs](https://docs.openclaw.ai/cron) <br>
- [MiniMax Official Feishu Documentation](https://vrfi1sk8a0.feishu.cn/wiki/YwEZwj3iuixCK9koFeacwvC6n9d) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with citations, diagnostic steps, and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Replies should match the user's language and avoid acting on high-risk configuration or external-send operations without explicit authorization.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
