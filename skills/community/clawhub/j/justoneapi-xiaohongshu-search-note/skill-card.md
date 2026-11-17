## Description:

Call Xiaohongshu (RedNote) note search endpoints through JustOneAPI by keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Xiaohongshu (RedNote) notes by keyword through JustOneAPI, with optional filters for endpoint version, page, sort order, note type, and note publish time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JustOneAPI tokens may be exposed through command-line arguments, shell history, process logs, proxy logs, or API request logs.

Mitigation: Use a short-lived, low-scope token, avoid logging command invocations or full request URLs, and rotate the token if exposure is suspected.

Risk: Search terms and filters are sent to JustOneAPI when the skill calls Xiaohongshu note search endpoints.

Mitigation: Install and use the skill only when sharing those lookup terms with JustOneAPI is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-search-note)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_note&utm_content=project_link)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_note&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, json]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks for missing required parameters, reports the operation ID and endpoint path used, summarizes results before raw JSON, and includes API error payloads when requests fail.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
