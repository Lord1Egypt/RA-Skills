## Description:

卖家之家(跨境电商)活动查询与发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjzj-tec](https://clawhub.ai/user/mjzj-tec)

### License/Terms of Use:

MIT-0

## Use Case:

External agents use this skill to query MJZJ cross-border e-commerce activities, retrieve activity cities, upload event images, and publish activity records through MJZJ APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload user images and publish event records to a remote MJZJ service.

Mitigation: Review event fields and image files before use, require explicit confirmation before using upload URLs or calling createActivity, and use a scoped or revocable MJZJ API key where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mjzj-tec/skills/mjzj-activity)
- [MJZJ activity page](https://mjzj.com/activity)
- [MJZJ agent API key page](https://mjzj.com/user/agentapikey)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MJZJ_API_KEY for city lookup, uploads, and publishing; public activity queries do not require a token.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
