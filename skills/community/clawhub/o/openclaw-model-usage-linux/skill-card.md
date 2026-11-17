## Description:

Track OpenClaw AI token usage and cost per model on Linux by parsing session JSONL files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiyouwolegequ](https://clawhub.ai/user/aiyouwolegequ)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to summarize local OpenClaw model usage, token counts, channel activity, and estimated cost from Linux session logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the local OpenClaw session store and may inspect conversation text while classifying channels.

Mitigation: Install only in environments where local session-log access is acceptable, and review the skill before use.

Risk: The skill saves aggregate usage history under the user's OpenClaw workspace.

Mitigation: Review or remove shipped and generated state files before use when prior usage history should not influence reporting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiyouwolegequ/skills/openclaw-model-usage-linux)
- [Publisher profile](https://clawhub.ai/user/aiyouwolegequ)

## Skill Output:

**Output Type(s):** [text, json, shell commands, analysis]

**Output Format:** [Console text summary with documented JSON output option]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports turns, input tokens, output tokens, cache read/write tokens, model usage, channel usage, daily cost, and estimated cost in USD or RMB.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
