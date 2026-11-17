## Description:

Tracks OpenClaw token usage and API costs from local session data, preferring openclaw-cost-diff for current cost analysis and comparisons while keeping the bundled Python script as a fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfrederiksen](https://clawhub.ai/user/pfrederiksen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect local session data for token spend, model-level cost breakdowns, daily trends, and window-over-window cost regressions without API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default workflow invokes a separate local openclaw-cost-diff executable that is not included in the reviewed artifact.

Mitigation: Verify the external CLI's source, version, ownership, permissions, and checksum before use, or run the bundled scripts/cost_tracker.py fallback instead.

Risk: Cost analysis reads local OpenClaw session data that may contain sensitive usage history.

Mitigation: Run as a non-root user with read-only access limited to the required OpenClaw session data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pfrederiksen/skills/openclaw-cost-tracker)
- [OpenClaw](https://openclaw.ai)
- [Bundled fallback script](scripts/cost_tracker.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash commands and optional JSON cost reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local OpenClaw session JSONL data; no API keys required.]

## Skill Version(s):

1.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
