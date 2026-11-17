## Description:

Magpie helps an agent query Chinese A-share quotes, fund flows, K-line data, watchlists, alert rules, portfolio digests, and 龙虎榜 data through a trusted local magpie daemon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[symbolstar](https://clawhub.ai/user/symbolstar)

### License/Terms of Use:

MIT-0

## Use Case:

Users who already run the local magpie daemon can use this skill to monitor Chinese A-share prices, fund flows, K-line history, watchlists, alerts, and market digests. It supports data lookup and local alert management, but is not for trading execution, technical analysis, news analysis, or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local watchlist and alert history through the magpie daemon.

Mitigation: Use it only with a magpie daemon you run and trust, and avoid exposing local financial-monitoring data in sessions where that is not intended.

Risk: The skill can add or remove local watchlist and alert rules when prompted.

Mitigation: Confirm ambiguous stock codes, thresholds, and requested actions before creating, changing, or deleting alert and watchlist entries.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise Markdown responses with optional shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted local magpie daemon at http://127.0.0.1:17891 and a successful health check before use.]

## Skill Version(s):

0.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
