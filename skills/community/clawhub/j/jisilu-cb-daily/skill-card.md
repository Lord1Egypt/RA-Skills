## Description:

每日从集思录 webapi 抓取可转债基本数据、强赎倒计时、下修倒计时，支持Cookie管理和本地持久化存储。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cchunter](https://clawhub.ai/user/cchunter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect daily Jisilu convertible bond data, merge redemption and conversion-price-adjustment countdown fields, and save a dated local CSV for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable Jisilu login cookies may expose the account if pasted into shared chats, logs, or files with broad read access.

Mitigation: Use the skill only in a trusted local environment, restrict access to references/cookie.json and generated logs, avoid sharing cookie values, and refresh or revoke the Jisilu session after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cchunter/skills/jisilu-cb-daily)
- [Jisilu](https://www.jisilu.cn/)
- [Jisilu convertible bond list API](https://www.jisilu.cn/webapi/cb/list/)
- [Jisilu convertible bond redemption API](https://www.jisilu.cn/webapi/cb/redeem/)
- [Jisilu convertible bond adjustment API](https://www.jisilu.cn/webapi/cb/adjust/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands, terminal status text, and dated CSV output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates output/jisilu_cb_YYYY-MM-DD.csv and may persist reusable Jisilu login cookies in references/cookie.json.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
