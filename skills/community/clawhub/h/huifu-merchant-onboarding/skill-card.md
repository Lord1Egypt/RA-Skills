## Description:

帮助开发者按汇付官方资料处理商户进件、用户开户与业务入驻，并核对字段、SDK 和状态。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huifu](https://clawhub.ai/user/huifu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers integrating Huifu merchant onboarding or user account opening use this skill to select the appropriate API, check field and SDK contracts, and troubleshoot application status. It supports enterprise, individual, and small-merchant onboarding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment marks the release suspicious and partial, citing TLS verification exceptions and image upload examples that omit validation.

Mitigation: Follow the security guidance: do not install until the TLS verification exception is removed and upload examples require validation; treat the partial scan as incomplete.

## Reference(s):

- [Merchant onboarding overview](references/shared-overview.md)
- [Merchant onboarding field contracts](references/merchant-onboarding-field-contracts.md)
- [Signing and verification guidance](references/shared-signing-v2.md)
- [Official Huifu merchant service source index](references/official-service-source-index.md)
- [Huifu enterprise merchant onboarding API documentation](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_qyshjbxxrz_kyc.md)
- [Huifu Open Platform](https://paas.huifu.com/open/home/index.html)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions]

**Output Format:** [Markdown with field guidance and Java, PHP, or Python SDK examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include implementation TODOs where official contracts need confirmation.]

## Skill Version(s):

1.2.0 (source: release evidence; references/skill-version-policy.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
