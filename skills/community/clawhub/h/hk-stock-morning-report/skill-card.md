## Description:

Generates a Hong Kong stock market morning report for bank trading desks using market data, news search, and a fixed report template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjlrestlong-ai](https://clawhub.ai/user/cjlrestlong-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Bank trading-desk users and agents use this skill to assemble a daily Hong Kong stock morning report with market review, southbound capital flow, current news, and one highlighted Hong Kong stock.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can forward an internal-labeled report to WeChat and Feishu without clear recipient controls or per-send confirmation.

Mitigation: Use only where web access is allowed, output paths are controlled, and WeChat or Feishu recipients are explicitly configured and confirmed before each send.

Risk: The skill relies on current market data and news searches, so stale or unsupported information can produce misleading report content.

Mitigation: Review the generated report against the cited sources and the bundled format and error checklists before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjlrestlong-ai/skills/hk-stock-morning-report)
- [stock_report_format.md](references/stock_report_format.md)
- [errors.md](references/errors.md)
- [Tencent Finance quote API](https://qt.gtimg.cn/q={code})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown report text with supporting shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report content depends on current market data, current news search results, and configured WeChat or Feishu recipients.]

## Skill Version(s):

1.4.11 (source: server-resolved release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
