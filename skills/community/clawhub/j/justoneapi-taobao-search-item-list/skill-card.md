## Description:

Call GET /api/taobao/search-item-list/v1 for Taobao and Tmall Product Search through JustOneAPI with keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to search Taobao and Tmall product listings through JustOneAPI by keyword, with optional filters for sort order, Tmall-only results, price range, and page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is sensitive and is passed to the helper for the API request.

Mitigation: Use a narrowly scoped or replaceable token when possible, avoid exposing command logs or screenshots, and rotate the token if exposure is suspected.

Risk: Search keywords and filters are sent to the JustOneAPI service as query parameters.

Mitigation: Review parameters before execution and avoid using sensitive search terms unless the deployment policy allows sharing them with the API provider.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_search_item_list&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_search_item_list&utm_content=project_link)
- [Generated operations reference](generated/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples; helper output is formatted JSON from the API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; keyword is required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
