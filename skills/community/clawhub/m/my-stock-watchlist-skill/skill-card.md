## Description:

This skill helps an agent manage a stock watchlist stored in a specified DingTalk multidimensional table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canonxu](https://clawhub.ai/user/canonxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add, delete, and query stock tickers in a DingTalk stock watchlist when the request explicitly concerns a watchlist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can add or delete rows in the configured DingTalk watchlist table.

Mitigation: Confirm the Base ID, Sheet ID, stock-code field name, and requested ticker before executing add or delete operations.

## Reference(s):

- [DingTalk watchlist table](https://alidocs.dingtalk.com/i/nodes/1OQX0akWmxpyBpnaCQQQoYkY8GlDd3mE)
- [ClawHub skill page](https://clawhub.ai/canonxu/skills/my-stock-watchlist-skill)

## Skill Output:

**Output Type(s):** [Text, API Calls, JSON, Guidance]

**Output Format:** [Natural-language responses with DingTalk table API requests and JSON record data when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can add, list, and delete rows in the configured DingTalk table through the dependent dingtalk-ai-table skill.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
