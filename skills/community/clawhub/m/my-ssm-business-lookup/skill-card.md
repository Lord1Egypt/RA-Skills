## Description:

Look up Malaysian company registration data from SSM and return directors, status, filings, and business type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wms2537](https://clawhub.ai/user/wms2537)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to look up Malaysian business registration records by company name or registration number and receive structured company details for review or downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each lookup charges the supplied user ID, and the security evidence notes limited authorization around that billing context.

Mitigation: Require explicit user consent for each charge and bind billing to authenticated user context rather than accepting a raw user_id alone.

Risk: The skill makes network calls to an SSM lookup service and paid billing flow.

Mitigation: Disclose and constrain the SSM lookup endpoint and SkillPay billing dependency before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wms2537/skills/my-ssm-business-lookup)
- [Publisher profile](https://clawhub.ai/user/wms2537)
- [Skill homepage](https://github.com/swmeng/myskills)
- [SSM lookup endpoint](https://ssm-api.swmengappdev.workers.dev)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Structured JSON responses with company lookup data or payment and error details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLPAY_API_KEY and charges $0.05 USDT per call via SkillPay.me.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
