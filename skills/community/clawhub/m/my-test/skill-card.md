## Description: <br>
Captures learnings, errors, feature requests, and corrections so agents can preserve and promote useful knowledge across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LuckyJin](https://clawhub.ai/user/LuckyJin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to log command failures, user corrections, missing capabilities, and reusable best practices, then promote durable learnings into agent memory or instruction files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation-derived details and future-agent instructions too broadly. <br>
Mitigation: Keep .learnings private or gitignored, avoid storing secrets or customer data, and manually review promotions into persistent agent instruction files. <br>
Risk: Optional hooks can inject learning reminders across projects or prompts more broadly than intended. <br>
Mitigation: Enable hooks only after reviewing the scripts and narrowing their matchers to the projects and prompts where persistent learning capture is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LuckyJin/my-test) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update learning log files and optional hook reminders when configured by the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
