## Description:

Call GET /api/taobao/get-item-comment/v3 for Taobao and Tmall Product Reviews through JustOneAPI with itemId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to call JustOneAPI's Taobao/Tmall product review endpoint, using an itemId to retrieve review data for feedback analysis and product research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through command arguments, request URLs, command logs, screenshots, or shared transcripts.

Mitigation: Use a narrowly scoped or disposable token, avoid sharing command logs or request URLs, and rotate the token if exposure is suspected.

Risk: The skill depends on a JustOneAPI token and network access to retrieve Taobao/Tmall review data.

Mitigation: Install and run it only when the user is comfortable granting that API access for product review lookups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-taobao-get-item-comment)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_get_item_comment&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_get_item_comment&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, API Calls, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs identify the operation ID and endpoint path, summarize the itemId lookup scope, and may include the raw backend JSON response.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
