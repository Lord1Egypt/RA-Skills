## Description:

卖家之家(跨境电商)货盘搜索与发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjzj-tec](https://clawhub.ai/user/mjzj-tec)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace sellers and operators use this skill to search MJZJ pallet listings, review label groups, submit pallet publish applications with uploaded images, and check their own pallets or pending applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated requests can read account-specific pallet and application data.

Mitigation: Use the skill only with an MJZJ_API_KEY intended for this workflow, and treat returned account and listing data as sensitive business information.

Risk: Publish applications upload user-provided images and submit listing details to MJZJ for review.

Mitigation: Review listing details and image files before asking the agent to submit a publish application.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mjzj-tec/skills/mjzj-huo)
- [MJZJ pallet marketplace](https://mjzj.com/gongxu)
- [MJZJ agent API key page](https://mjzj.com/user/agentapikey)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MJZJ_API_KEY for authenticated marketplace management requests; public pallet search endpoints do not require a token.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
