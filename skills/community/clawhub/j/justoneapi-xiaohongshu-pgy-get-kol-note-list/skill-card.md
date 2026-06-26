## Description: <br>
Call GET /api/xiaohongshu-pgy/get-kol-note-list/v1 for Xiaohongshu Creator Marketplace (Pugongying) Creator Note List through JustOneAPI with adSwitch, kolId, and orderType. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and analysts use this skill to retrieve Xiaohongshu Creator Marketplace creator note metadata, publish times, and engagement indicators through JustOneAPI for content analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token is passed through the helper and sent as a query parameter, which can expose it through local process inspection, shell history, or URL logs. <br>
Mitigation: Use a restricted JustOneAPI token, avoid logging commands or request URLs, and prefer changing the helper to read the token from an environment variable or stdin and use an Authorization header if supported. <br>
Risk: Raw endpoint responses and backend error payloads may include creator analytics or operational details that should not be shared broadly. <br>
Mitigation: Review response and error payloads before sharing them, and avoid pasting raw outputs into public tickets, chat, or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-pgy-get-kol-note-list) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_note_list&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON from the JustOneAPI endpoint] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; required request parameters are kolId, adSwitch, and orderType.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
