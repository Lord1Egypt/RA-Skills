## Description: <br>
Call GET /api/weixin/get-article-detail/v1 for WeChat Official Accounts Article Details through JustOneAPI with articleUrl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch WeChat Official Accounts article details from JustOneAPI by articleUrl for archiving, research, and content analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a reusable JustOneAPI token in command arguments and request URLs, which can expose credentials through logs, shell history, process listings, or upstream request records. <br>
Mitigation: Use only scoped, rotatable tokens in trusted environments; avoid logging command invocations; and prefer a future version that reads the token internally from the environment and sends it in an Authorization header. <br>
Risk: Submitted article URLs are sent to JustOneAPI and may identify private or sensitive content. <br>
Mitigation: Submit only article URLs that are appropriate to share with JustOneAPI and avoid private article URLs unless that disclosure is acceptable. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_article_detail&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_article_detail&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON from the API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and an articleUrl parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
