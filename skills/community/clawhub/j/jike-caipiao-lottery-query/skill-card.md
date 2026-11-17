## Description:

查询彩票最新开奖、指定彩种期开奖详情、福彩3D/排列3历史号码和冷热号统计；数据由即刻数据开放接口提供，仅用于开奖信息查询，不提供预测或投注建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query published Chinese lottery results, draw details, historical three-digit number occurrences, and hot/cold number statistics from JikeAPI. It is intended for factual draw-data lookup and should not be used for betting predictions or wagering advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Jike API AppKey is sensitive and is sent in request URLs.

Mitigation: Provide the key through a host-managed environment variable, avoid committing scripts/.env, and restrict access to command logs or network traces that may contain request URLs.

Risk: Changing JIKE_API_BASE_URL can send the AppKey to a non-Jike host.

Mitigation: Leave JIKE_API_BASE_URL unset unless the destination is explicitly trusted and reviewed.

Risk: Lottery statistics may be misused as betting advice.

Mitigation: Use outputs only for factual draw lookup and keep responses from making predictions or wagering recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-caipiao-lottery-query)
- [JikeAPI homepage](https://www.jikeapi.cn/)
- [JikeAPI lottery latest endpoint](https://api.jikeapi.cn/v1/caipiao/lottery/latest)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Terminal text tables or raw JSON, with setup guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a Jike API AppKey provided through JIKE_CAIPIAO_LOTTERY_QUERY_KEY or JIKE_APPKEY.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
