## Description: <br>
Looks up Chinese words through Jike API endpoints, including search, details, random words, synonyms, and antonyms with pinyin, explanations, sources, examples, usage, synonyms, and antonyms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to answer Chinese word lookup questions, retrieve word details, and find synonyms or antonyms from Jike's word APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Jike AppKey, which could be exposed if passed on the command line or stored in shared directories. <br>
Mitigation: Prefer JIKE_WORD_QUERY_KEY or JIKE_APPKEY environment variables and keep credentials out of shared script directories. <br>
Risk: JIKE_API_BASE_URL can redirect requests to a replacement endpoint. <br>
Mitigation: Leave JIKE_API_BASE_URL unset unless the replacement endpoint is deliberately trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-word-query) <br>
- [Publisher profile](https://clawhub.ai/user/jikeapi-cn) <br>
- [Jike API homepage](https://www.jikeapi.cn/) <br>
- [Jike word query API endpoint](https://api.jikeapi.cn/v1/word/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text tables or JSON from a Python command-line script, with Markdown usage guidance in the skill instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JIKE_WORD_QUERY_KEY or JIKE_APPKEY credential; JIKE_API_BASE_URL can override the default API host.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
