## Description:

Aggregates and delivers curated briefings about releases, skills, security issues, community discussions, and ecosystem news in the OpenClaw ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw ecosystem participants use this skill to collect scheduled or on-demand briefings about OpenClaw releases, registry updates, security items, community discussion, and related news.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled or on-demand runs make network checks against GitHub, ClawHub, and web search sources and may deliver results to a configured channel.

Mitigation: Install only when those network checks and deliveries are intended, and review the cron schedule and delivery channel before enabling the skill.

Risk: Briefing state is stored locally and can cause ongoing or repeated news monitoring if left enabled.

Mitigation: Remove the cron entry or delete the state files when ongoing briefings are no longer wanted.

## Reference(s):

- [OpenClaw News skill page](https://clawhub.ai/arc-claw-bot/skills/openclaw-news)
- [Arc from Fulcra.ai publisher profile](https://clawhub.ai/user/arc-claw-bot)
- [ClawHub registry](https://www.clawhub.ai)
- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefing with supporting JSON state and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses incremental local state to avoid repeating previously reported items.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
