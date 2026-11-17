## Description:

High-conviction AI trading signals - only the strongest ETF calls from 6 opposing analysts. Free, no API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredxyt](https://clawhub.ai/user/fredxyt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch public MoltStreet ETF alert data and summarize only high-conviction trading signals or ticker details. Outputs should be treated as informational market signal summaries, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake AI-generated ETF signals for financial advice.

Mitigation: Present MoltStreet results as informational market signals, include the not-financial-advice disclaimer, and avoid framing outputs as investment recommendations.

Risk: Agents may fetch external market signal data for vague market questions where the user did not ask for alert data.

Mitigation: Call the skill only when the user explicitly asks for alerts, strong signals, top picks, best opportunities, or a quick signal-focused market summary.

Risk: Signal data may be stale or unavailable because updates are not real-time and some days have no high-conviction signals.

Mitigation: Tell users when no signals pass the threshold and avoid implying real-time quote coverage.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fredxyt/skills/moltstreet-alerts)
- [Publisher profile](https://clawhub.ai/user/fredxyt)
- [MoltStreet homepage](https://moltstreet.com)
- [MoltStreet skill documentation](https://moltstreet.com/skill.md)
- [MoltStreet disclaimer](https://moltstreet.com/disclaimer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and concise market-alert summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public MoltStreet API data with curl; no API key is required.]

## Skill Version(s):

1.0.1 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
