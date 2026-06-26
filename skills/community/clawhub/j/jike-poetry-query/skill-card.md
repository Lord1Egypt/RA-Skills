## Description: <br>
唐诗宋词元曲查询，支持古诗词列表、详情、诗人查询、诗人详情、随机诗词、词牌信息、朝代列表、类别列表和体裁列表，数据由即刻数据（jikeapi.cn）开放接口提供。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to look up Tang poetry, Song lyrics, and Yuan songs by title, author, dynasty, category, or form, and to retrieve poem details, poet information, random poems, tune patterns, dynasty lists, category lists, and genre lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Poetry titles, author names, and related query parameters are sent to jikeapi.cn with a Jike API key. <br>
Mitigation: Install only if that data sharing is acceptable, use a dedicated low-privilege API key, and avoid submitting sensitive lookup terms. <br>
Risk: The API base URL can be overridden with JIKE_API_BASE_URL. <br>
Mitigation: Keep JIKE_API_BASE_URL unset unless you intentionally trust the alternate endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-poetry-query) <br>
- [Jike API homepage](https://www.jikeapi.cn/) <br>
- [Jike poetry query endpoint](https://api.jikeapi.cn/v1/poetry/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON from command-line poetry lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JIKE_POETRY_QUERY_KEY or JIKE_APPKEY API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
