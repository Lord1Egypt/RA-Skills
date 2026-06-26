## Description: <br>
Call GET /api/web/html/v1 for Web Page HTML Content through JustOneAPI with url. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch the HTML content of a specified web page through JustOneAPI. It is suited for workflows that need page HTML returned from the documented `htmlV1` endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token may be exposed through command-line or query-string token handling. <br>
Mitigation: Use a narrowly scoped token, avoid pasting token values into chat or logs, and prefer a revised release that reads the token from the environment or sends it in headers. <br>
Risk: Requested URLs are sent to JustOneAPI and may disclose sensitive internal, authenticated, or pre-signed resources. <br>
Mitigation: Use only URLs appropriate to share with JustOneAPI and avoid sensitive internal, authenticated, or pre-signed URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-web-html) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web_html&utm_content=project_link) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web_html&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown usage guidance with a Node.js command invocation and JSON API output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires `node`, a `JUST_ONE_API_TOKEN`, and a `url` query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
