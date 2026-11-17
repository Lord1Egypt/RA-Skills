## Description:

实时诊断股票持仓，调用腾讯行情数据并结合技术指标计算买入评分、卖出评分、PASS/FAIL 状态、操作信号和盈亏情况。

This skill is for research and development only.

## Publisher:

[jayden-zhong](https://clawhub.ai/user/jayden-zhong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze a supplied stock holdings list, retrieve market data, compute technical scores, and identify hold, warn, or sell signals for portfolio review. The artifact states that the analysis is for learning and research and does not constitute investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill runs code from hardcoded external .qclaw workspace paths and can load replacement modules outside the reviewed package.

Mitigation: Review before installing, run only when every referenced workspace file is trusted, and prefer a packaged version that reads holdings from explicit JSON or CSV inputs.

Risk: Stock analysis output can be mistaken for investment advice.

Mitigation: Use the output as informational portfolio review, confirm market data and decisions independently, and keep the non-advice disclaimer visible to users.

Risk: Live market-data requests can fail or return incomplete data, which may leave prices, scores, or signals missing.

Mitigation: Check generated JSON and text summaries for missing or zero-valued fields before relying on the analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jayden-zhong/skills/holdings-analysis)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text and JSON analysis summaries with Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local holdings analysis files and depends on live market data availability.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
