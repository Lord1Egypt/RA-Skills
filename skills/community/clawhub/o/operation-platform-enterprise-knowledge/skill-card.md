## Description:

Looks up merchant IDs by sending a parsed seller name and local OpenClaw username to a Kuaishou internal CRM endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimadara](https://clawhub.ai/user/jimadara)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized Kuaishou operations or CRM users can use this skill to resolve merchant IDs from seller names. It requires a locally configured OpenClaw username and returns the service response directly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is labeled as domain testing, but server security evidence says it performs merchant CRM lookup.

Mitigation: Install only when the intended use is authorized Kuaishou merchant CRM lookup, and rename or scope the skill before general use.

Risk: The skill reads a local OpenClaw username and sends it with the parsed seller name to an internal corporate endpoint.

Mitigation: Use only in approved environments with authorized user credentials and merchant data handling approval.

Risk: The skill returns raw backend data directly to the user.

Mitigation: Review returned data for sensitivity before sharing or using it outside the authorized workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimadara/skills/operation-platform-enterprise-knowledge)
- [Kuaishou merchant CRM seller search endpoint](https://merchant-lego.corp.kuaishou.com/gateway/crm/seller/manager/querySellerSearchResult)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Raw API response or error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns backend data directly; no post-processing is described.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
