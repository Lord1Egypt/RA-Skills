## Description:

按城市查二手房与新房参考均价、环比同比及近月走势（可生成列表与 SVG 折线图）。当用户说：长沙房价多少？深圳二手房均价走势？给个查房价链接，或类似城市房价问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer city house-price questions in Chinese, including second-hand and new-home reference averages, month-over-month and year-over-year movement, trend lists, and direct Fangjia city links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can fetch URLs broader than the core city-slug workflow requires.

Mitigation: Use only trusted fangjia.fang.com city URLs or known city slugs, and avoid allowing untrusted users to supply arbitrary URLs.

Risk: Optional chart generation can write a local HTML file.

Mitigation: Do not let untrusted requests choose the chart output path; keep generated files in an expected workspace location.

Risk: Network scraping can be unreliable or inappropriate at high frequency.

Mitigation: Use the skill for low-frequency, compliant lookups and preserve the source caveat that values are platform reference data, not official government or transaction prices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/house-price)
- [Publisher profile](https://clawhub.ai/user/jisuapi)
- [Fangjia house-price source](https://fangjia.fang.com/)
- [Jisu API publisher site](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, files, guidance]

**Output Format:** [Chinese Markdown or plain text summaries with optional shell commands, monthly trend lists, stdout SVG, and optional HTML chart files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper can fetch Fangjia city pages and trend endpoints; optional chart generation writes an HTML file only when requested.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
