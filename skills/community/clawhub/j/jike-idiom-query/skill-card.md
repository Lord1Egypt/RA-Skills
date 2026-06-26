## Description: <br>
成语词典技能，支持搜索成语、查询成语详情、随机成语和成语接龙，并返回拼音、解释、出处、例句、故事、用法、近义词和反义词。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI agent developers use this skill to answer Chinese idiom questions, look up idiom details, retrieve random idioms, and support idiom-chain play through JikeAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Idiom queries and the configured AppKey are sent to the JikeAPI service. <br>
Mitigation: Install only if the user trusts JikeAPI and is comfortable sending idiom queries and the AppKey to that service. <br>
Risk: The JIKE_API_BASE_URL environment variable can redirect traffic, including the AppKey, away from the default JikeAPI endpoint. <br>
Mitigation: Do not set JIKE_API_BASE_URL unless intentionally redirecting traffic to a trusted endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-idiom-query) <br>
- [JikeAPI homepage](https://www.jikeapi.cn/) <br>
- [JikeAPI idiom query endpoint](https://api.jikeapi.cn/v1/idiom/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [Plain text tables and detail summaries, with optional formatted JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JIKE_IDIOM_QUERY_KEY or JIKE_APPKEY value; the API base URL can be overridden with JIKE_API_BASE_URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
