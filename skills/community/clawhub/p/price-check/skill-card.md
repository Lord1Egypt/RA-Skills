## Description:

Price-check searches major Chinese e-commerce platforms for live product prices, filters noisy listings, tracks local price history, and returns a buy-or-wait recommendation with purchase links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuxiaoyang2007-prog](https://clawhub.ai/user/yuxiaoyang2007-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping agents use this skill to compare prices across Chinese e-commerce marketplaces, screen out noisy or mismatched listings, and decide whether a product is worth buying now.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product searches may be sent to maishou88.com.

Mitigation: Use the skill only for queries acceptable to share with that external service, and avoid sensitive procurement or personal shopping searches.

Risk: Local query history is retained in a SQLite database.

Mitigation: Review retention needs before deployment, clear the local data directory when needed, or configure the history provider to noop if local retention is not acceptable.

Risk: Optional Feishu sync can send shopping queries and results to a Feishu workspace and relies on plaintext local configuration.

Mitigation: Keep Feishu sync disabled unless explicitly approved, restrict Bitable permissions, and protect the local config file containing Feishu tokens or table identifiers.

Risk: The skill attempts to control the agent's final response by requiring exact rendering of its report field.

Mitigation: Treat the report as data to preserve where useful, while still applying the agent platform's policy, security, and user-context requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuxiaoyang2007-prog/skills/price-check)
- [Project homepage](https://github.com/yuxiaoyang2007-prog/price-check)
- [Report template](references/report-template.md)
- [Configuration example](config.example.json)
- [shopmind-price-compare dependency attribution](https://clawhub.ai/skills/shopmind-price-compare)
- [Upstream author profile](https://clawhub.ai/users/xiaohaook)
- [OpenClaw runtime](https://openclaw.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON with a human-facing Markdown report field; --report emits Markdown only.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes live price candidates, filtering details, verdicts, purchase/search links, local history summaries, and optional Feishu sync records.]

## Skill Version(s):

0.6.4 (source: server release evidence and CHANGELOG, released 2026-04-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
