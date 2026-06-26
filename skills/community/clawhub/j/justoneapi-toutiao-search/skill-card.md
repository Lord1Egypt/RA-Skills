## Description: <br>
Call 2 search versions for Toutiao App Keyword Search through JustOneAPI with keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to search Toutiao app and web results through JustOneAPI by keyword for topic discovery, trend research, and monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords and the JustOneAPI token are sent to JustOneAPI when a request is made. <br>
Mitigation: Use a limited-scope or revocable JustOneAPI token where possible and only send search terms approved for the service. <br>
Risk: Passing the token as a command-line argument can expose it on shared systems where process arguments are visible. <br>
Mitigation: Run the helper only on trusted systems and avoid shared environments when handling sensitive tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-toutiao-search) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao_search&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao_search&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Short Markdown summary followed by raw JSON from the selected API operation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [States the operation ID and endpoint path used; includes backend error payloads with the exact operation ID when requests fail.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
