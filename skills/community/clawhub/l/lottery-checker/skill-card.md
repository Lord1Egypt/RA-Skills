## Description:

中国体育彩票查奖工具（大乐透批量查询）。检查用户提供的大乐透号码是否中奖，支持单注或多注批量查询，自动生成报表，显示各奖项中奖人数和金额。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sudaqinnishui](https://clawhub.ai/user/sudaqinnishui)

### License/Terms of Use:


## Use Case:

External users and agents can use this skill to check one or more China Sports Lottery Super Lotto tickets against the latest draw and produce a readable prize report. Treat results as informational and verify potential winnings through official lottery channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script disables TLS certificate verification when fetching lottery results.

Mitigation: Restore certificate verification before relying on the output, especially for financially relevant decisions.

Risk: Lottery results and prize information may be incorrect, stale, or unsuitable as the sole basis for claiming winnings.

Mitigation: Use the report as informational and verify any potential winnings through official China Sports Lottery channels or local lottery offices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sudaqinnishui/skills/lottery-checker)
- [China Sports Lottery API endpoint](https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry)
- [China Sports Lottery website](https://www.lottery.gov.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Console text report or JSON, with Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts single-ticket or batch Super Lotto number input.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
