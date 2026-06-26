## Description: <br>
双色球幸运号码预测 - 基于天干地支阴阳五行+随机森林机器学习模型。根据用户输入的彩票开奖日期，计算八字并生成推荐号码。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[landyun](https://clawhub.ai/user/landyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to generate entertainment-oriented Double Color Ball lottery number predictions, bazi and five-element analysis, model scoring tables, and prior-prediction comparison summaries for a requested draw date. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep a local history of lottery predictions and compare it against web-searched results. <br>
Mitigation: Confirm before allowing memory-file reads or writes, and only use web lookup for prior draw results when that behavior is expected. <br>
Risk: Hardcoded local file paths may not match the user's environment. <br>
Mitigation: Review and adjust local memory and history-data paths before running prediction or backtest workflows. <br>
Risk: Lottery predictions can be misunderstood as betting advice despite the skill's entertainment framing. <br>
Mitigation: Present outputs as entertainment-only analysis and preserve the disclaimer that lottery outcomes are random and not scientifically predictable. <br>


## Reference(s): <br>
- [Luckyball release page](https://clawhub.ai/landyun/luckyball) <br>
- [landyun publisher profile](https://clawhub.ai/user/landyun) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with prediction tables, analysis summaries, recommended numbers, and model status details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local prediction-history comparison output when prior records are available.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
