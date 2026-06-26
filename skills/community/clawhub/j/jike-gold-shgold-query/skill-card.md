## Description: <br>
Queries historical Shanghai Gold Exchange market data by date through JikeAPI, returning instruments, open, high, low, close, change, percentage change, and volume. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to fetch date-specific Shanghai Gold Exchange historical quotes from JikeAPI and present the results as a table or JSON. It is intended for information lookup and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The queried date and JikeAPI AppKey are sent to JikeAPI when the lookup runs. <br>
Mitigation: Prefer environment variables over command-line keys, restrict any local .env file, avoid logging credentials, and rotate the key if it appears in logs or shared shell history. <br>
Risk: Market data may be incomplete, delayed, or inappropriate for direct financial decision-making. <br>
Mitigation: Present results as informational lookup data, keep the skill's no-investment-advice notice, and verify critical values with an authoritative market-data source before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-gold-shgold-query) <br>
- [JikeAPI homepage](https://www.jikeapi.cn/) <br>
- [JikeAPI Shanghai Gold Exchange history endpoint](https://api.jikeapi.cn/v1/gold/shgold/history) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal table or JSON payload, usually summarized as Markdown by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JikeAPI AppKey via JIKE_GOLD_SHGOLD_QUERY_KEY or JIKE_APPKEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
