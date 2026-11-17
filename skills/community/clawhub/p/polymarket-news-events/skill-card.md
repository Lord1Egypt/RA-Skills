## Description:

Monitors premium RSS feeds for breaking news, matches stories to Polymarket markets with keyword analysis, and can generate or execute trade signals when estimated impact exceeds a configured threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mibayy](https://clawhub.ai/user/mibayy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor breaking news feeds and identify Polymarket market opportunities. In live mode, it can place automated real-money trades through Simmer using configured credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place repeated real-money trades based on external RSS feeds.

Mitigation: Keep dry-run mode enabled until feeds, thresholds, and market matching behavior are reviewed, and require explicit operational approval before using --live.

Risk: Trading safeguards may be weak or unavailable when market context checks fail.

Mitigation: Change safety checks to fail closed and use a least-privilege trading key with strict per-trade and daily limits.

Risk: External news feed content and unpinned dependencies can affect trading decisions.

Mitigation: Pin dependencies, review feed sources, and remove or replace plaintext RSS sources where transport or authenticity risk is unacceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mibayy/skills/polymarket-news-events)
- [Publisher Profile](https://clawhub.ai/user/mibayy)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Console logs and trade API calls from a Python automaton]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run mode is the default; live trading requires the --live flag and SIMMER_API_KEY.]

## Skill Version(s):

2.0.2 (source: server release evidence and clawhub.json; artifact frontmatter lists 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
