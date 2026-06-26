## Description: <br>
新华字典。支持拼音列表、部首列表、按拼音查汉字、按部首查汉字、汉字详情查询，返回汉字、拼音、部首、笔画、结构、繁体、异体字、同义词、反义词和形近字。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI clients and users use this skill to query Chinese dictionary data by pinyin, radical, or single character, including pronunciation, radical, stroke count, structure, variants, synonyms, antonyms, and similar-looking characters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API key can be redirected to an unintended network destination if JIKE_API_BASE_URL is changed. <br>
Mitigation: Leave JIKE_API_BASE_URL unset or set it only to https://api.jikeapi.cn in controlled environments. <br>
Risk: A broad reusable JIKE_APPKEY may expose more access than this dictionary lookup needs. <br>
Mitigation: Prefer a narrower JIKE_CHARACTER_QUERY_KEY when available and keep keys scoped to the deployment environment. <br>
Risk: The security verdict is suspicious and requires review before installation. <br>
Mitigation: Review the skill and its environment-variable configuration before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-character-query) <br>
- [即刻数据 homepage](https://www.jikeapi.cn/) <br>
- [即刻数据新华字典接口](https://api.jikeapi.cn/v1/character/chinese/detail) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text tables or JSON emitted by a Python CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Jike AppKey via JIKE_CHARACTER_QUERY_KEY or JIKE_APPKEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
