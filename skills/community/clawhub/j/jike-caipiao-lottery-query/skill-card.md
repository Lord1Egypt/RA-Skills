## Description: <br>
查询彩票最新开奖、指定彩种期开奖详情、福彩3D/排列3历史号码和冷热号统计；数据由即刻数据开放接口提供，仅用于开奖信息查询，不提供预测或投注建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve public lottery draw facts, issue details, three-digit lottery number history, and hot/cold number statistics from JikeAPI. It is for factual lookup only, not lottery prediction or betting advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs a JikeAPI AppKey, and full request URLs could expose the key if logged. <br>
Mitigation: Use the documented JIKE_CAIPIAO_LOTTERY_QUERY_KEY environment variable, avoid committing .env files, and rotate the AppKey if request URLs may have been logged. <br>
Risk: Lottery statistics may be mistaken for prediction or betting guidance. <br>
Mitigation: Use the skill only for public draw facts and statistics, and do not present results as predictions or betting advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-caipiao-lottery-query) <br>
- [JikeAPI homepage](https://www.jikeapi.cn/) <br>
- [JikeAPI lottery latest endpoint](https://api.jikeapi.cn/v1/caipiao/lottery/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Formatted terminal text or raw JSON from the JikeAPI lottery endpoints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JIKE_CAIPIAO_LOTTERY_QUERY_KEY AppKey; supports latest, detail, number-history, and number-stat commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
