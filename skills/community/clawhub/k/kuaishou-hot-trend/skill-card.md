## Description:

Collects public Kuaishou video, creator post, and comment data through keyword search, creator listing, and video comment retrieval for trend research, competitor monitoring, KOL discovery, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External content creators, marketers, MCN teams, and analysts use this agent to collect public Kuaishou data for topic research, competitor monitoring, KOL screening, and comment insight workflows. It is intended for public data only and requires a configured Guaikei API token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keywords, profile or video URLs, and returned Kuaishou comments or posts are shared with the Guaikei API provider.

Mitigation: Use the skill only when that data sharing is authorized, and avoid submitting sensitive business research beyond the intended analysis scope.

Risk: Collected results may be written to a local logs directory and can contain sensitive market or competitor research.

Mitigation: Protect the logs directory according to the sensitivity of the collected data and periodically delete results that are no longer needed.

Risk: The skill depends on a third-party API token for access.

Mitigation: Store GUAIKEI_API_TOKEN as an environment variable, avoid exposing it in prompts or logs, and rotate it if disclosure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/kuaishou-hot-trend)
- [Guaikei API access](https://www.guaikei.com)
- [Options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Status-bearing JSON with optional concise Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; successful runs may save JSON result files under a local logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
