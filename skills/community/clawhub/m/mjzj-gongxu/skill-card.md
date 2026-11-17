## Description:

Helps agents search, publish, refresh, and delete MJZJ cross-border ecommerce supply-demand posts through MJZJ APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjzj-tec](https://clawhub.ai/user/mjzj-tec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and ecommerce operators use this skill to let an agent query MJZJ supply-demand metadata and manage their own supply-demand posts. It supports publishing, refreshing, deleting, and listing account-owned posts when an MJZJ API key is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an MJZJ API key to publish, refresh, delete, and view account-owned supply-demand posts.

Mitigation: Install only when these account actions are intended, keep the API key scoped and private, and review publish, refresh, and delete requests before approval.

Risk: Expired, missing, or unauthorized credentials can cause failed or misleading account-data requests.

Mitigation: Treat 401, 403, and 409 responses as action-specific errors and follow MJZJ's API-key refresh and permission guidance instead of substituting web search results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mjzj-tec/skills/mjzj-gongxu)
- [MJZJ supply-demand page](https://mjzj.com/gongxu)
- [MJZJ agent API key page](https://mjzj.com/user/agentapikey)
- [MJZJ manual publish page](https://mjzj.com/gongxu/publish)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with curl command examples, endpoint mappings, and error-handling text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MJZJ_API_KEY for account-specific publish, refresh, delete, and private listing operations.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
