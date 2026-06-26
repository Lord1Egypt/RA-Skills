## Description: <br>
Searches or randomly returns Chinese "Ten Whys" questions and answers using the Jike Data open API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search for Chinese Q&A content by keyword or request a random Q&A result. It returns table text by default and JSON when structured output is requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords and the Jike AppKey are sent to the configured Jike API endpoint. <br>
Mitigation: Use only trusted endpoints, keep JIKE_API_BASE_URL unset unless deliberately overriding it, and avoid exposing the AppKey in shared command histories or logs. <br>
Risk: Returned Q&A content comes from an external API and may be incomplete, unavailable, or unsuitable for a specific answer. <br>
Mitigation: Review API responses before relying on them in user-facing explanations and fall back gracefully when the API returns errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-tenwhy-query) <br>
- [Jike Data homepage](https://www.jikeapi.cn/) <br>
- [Jike Ten Whys query endpoint](https://api.jikeapi.cn/v1/tenwhy/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text tables or JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JIKE_TENWHY_QUERY_KEY or JIKE_APPKEY credential; query supports keyword, page, and page-size parameters, while random uses no business parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
