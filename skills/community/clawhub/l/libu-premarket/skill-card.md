## Description:

Libu Premarket generates an A-share premarket map that combines capital-flow signals, financial filters, and technical indicators to identify sectors and stocks for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ygbeyond](https://clawhub.ai/user/ygbeyond)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill before A-share market open to prepare a data-backed watchlist and premarket report. It is intended for market research and decision support, not as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad file, network, and environment-variable access and may load code from another local skill directory.

Mitigation: Install only after reviewing the publisher, run in an environment where those permissions are acceptable, and avoid keeping an untrusted Tushare integration under ~/.openclaw/skills/tushare-finance/scripts/api_client.py.

Risk: Payment and licensing checks are weak security boundaries.

Mitigation: Treat payment validation as a convenience control, not a protection mechanism for sensitive data or trusted execution.

Risk: Dependencies are not fully pinned.

Mitigation: Review and pin dependency versions before use in managed or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ygbeyond/skills/libu-premarket)
- [Tushare Pro](https://tushare.pro)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown report with a JSON data file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes pre_market_data.json and prints a premarket report; results depend on cached or live market data.]

## Skill Version(s):

14.0.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
