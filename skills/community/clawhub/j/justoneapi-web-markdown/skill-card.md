## Description: <br>
Call GET /api/web/markdown/v1 for Web Page Markdown Content through JustOneAPI with url. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve the Markdown content of a web page through JustOneAPI by providing a target URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Target URLs are sent to JustOneAPI and may reveal private, intranet, localhost, presigned, or secret-containing locations. <br>
Mitigation: Use only URLs that are appropriate to share with JustOneAPI, and avoid private or secret-bearing URLs. <br>
Risk: The API token is passed through command-line arguments and a URL query parameter. <br>
Mitigation: Handle JUST_ONE_API_TOKEN as sensitive secret material and avoid exposing command invocations, logs, screenshots, or shell history that include the token. <br>


## Reference(s): <br>
- [JustOneAPI API Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web_markdown&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown summary followed by JSON response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; the endpoint requires a url query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
