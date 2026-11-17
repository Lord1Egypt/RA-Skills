## Description:

Monitor Minimax Coding Plan usage to stay within API limits, fetch current usage stats, provide status alerts, and show 5-hour sliding window status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanhaixuan](https://clawhub.ai/user/lanhaixuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check Minimax Coding Plan quota, monitor remaining usage in the current 5-hour window, and decide whether to proceed with larger AI tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends MINIMAX_API_KEY to www.minimaxi.com to retrieve quota information.

Mitigation: Install only if you trust www.minimaxi.com with the API key and use the script only for quota checks.

Risk: Cron examples can expose the API key to scheduled environments or write usage output to unsafe locations.

Mitigation: Adapt cron paths, intentionally scope the API key for cron, choose a safe log location, and document how to remove the scheduled job.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lanhaixuan/skills/minimax-usage-cn)
- [Publisher Profile](https://clawhub.ai/user/lanhaixuan)
- [Minimax Homepage](https://www.minimaxi.com)
- [Minimax Coding Plan Usage Endpoint](https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable terminal output or JSON from the usage-check script, with Markdown guidance in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and curl; supports --json/-j for programmatic output.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
