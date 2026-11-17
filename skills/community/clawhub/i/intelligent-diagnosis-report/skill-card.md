## Description:

This skill performs domain testing by resolving a parsed merchant name through an internal Kuaishou CRM lookup and returning the raw lookup result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimadara](https://clawhub.ai/user/jimadara)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or operators use this skill to test a merchant domain flow by extracting a seller name, using a local OpenClaw username, and returning merchant lookup results. It is not documented in the artifact as a diagnosis report generator despite the release display name.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use a local OpenClaw username when calling an internal CRM endpoint.

Mitigation: Require explicit confirmation before using local identity and document the identity source before normal installation.

Risk: The skill returns raw internal merchant lookup results.

Mitigation: Filter or redact returned data before exposing results to users.

Risk: The public release display name does not match the current domain-testing and merchant-lookup behavior.

Mitigation: Rename and document the skill as an internal merchant lookup or domain-testing tool before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimadara/skills/intelligent-diagnosis-report)
- [ClawHub publisher profile](https://clawhub.ai/user/jimadara)
- [Kuaishou CRM merchant lookup endpoint](https://merchant-lego.corp.kuaishou.com/gateway/crm/seller/manager/querySellerSearchResult)

## Skill Output:

**Output Type(s):** [text, JSON, API calls]

**Output Format:** [Raw text or JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the HTTP lookup result directly to the user without documented filtering.]

## Skill Version(s):

1.0.12 (source: server release evidence; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
