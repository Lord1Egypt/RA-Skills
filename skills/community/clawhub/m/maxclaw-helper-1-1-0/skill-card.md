## Description:

Usage guidance and runtime diagnostics for MaxClaw and OpenClaw questions, feature setup, configuration meaning, onboarding steps, failures, retry loops, and safety-sensitive operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wt865143010](https://clawhub.ai/user/wt865143010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to answer MaxClaw and OpenClaw usage questions, diagnose runtime failures, and decide when to stop and escalate when trusted documentation does not support a safe answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad help-style requests and provide guidance that is not relevant to the user's product context.

Mitigation: Verify that the answer applies to the user's MaxClaw or OpenClaw deployment before following configuration or integration guidance.

Risk: Troubleshooting advice can affect critical configuration, external sends, or irreversible operations.

Mitigation: Require explicit user authorization before modifying critical config, sending data externally, or taking irreversible action.

Risk: Repeated failed operations can create retry loops or obscure the root cause.

Mitigation: Stop after repeated failures, consult trusted documentation, and escalate when no exact trusted match is available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wt865143010/skills/maxclaw-helper-1-1-0)
- [OpenClaw official docs](https://docs.openclaw.ai/)
- [OpenClaw CLI docs](https://docs.openclaw.ai/cli)
- [OpenClaw gateway docs](https://docs.openclaw.ai/gateway)
- [OpenClaw channel docs](https://docs.openclaw.ai/channels)
- [OpenClaw skills docs](https://docs.openclaw.ai/skills)
- [OpenClaw cron docs](https://docs.openclaw.ai/cron)
- [MiniMax official Feishu documentation](https://vrfi1sk8a0.feishu.cn/wiki/YwEZwj3iuixCK9koFeacwvC6n9d)
- [Trusted Sources](references/trusted-sources.md)
- [Community Support Template](references/community-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with citations and inline commands when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the user's language and may redirect to official community support when trusted documentation is insufficient.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact metadata reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
