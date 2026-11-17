## Description:

精准寻标与获客引擎-寻标宝，当用户需要通过招投标数据进行客户拓展、寻找潜在采购单位或分析企业上下游时调用，重点调用企业合作客户及供应商查询接口，输出清晰的获客目标列表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng)

### License/Terms of Use:

MIT-0

## Use Case:

External business-development and market-research users can search tender notices and company relationships to build prospect lists and identify potential buyers, suppliers, and partners.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Device-registration privacy assurances and account-registration or recovery instructions are flagged for review; provider-side retention and deletion of device fingerprints are unverified.

Mitigation: Review the registration flow before installation, use a manually obtained API key to avoid hardware-derived identification when preferred, require explicit confirmation before changing an existing account or key, and ask the publisher to reconcile the privacy and recovery guidance.

Risk: Data queries consume account credits, and temporary login links grant account access.

Mitigation: Check credit usage before data queries and treat generated login links as sensitive account-access credentials.

## Reference(s):

- [Tender search API reference](artifact/references/api-search.md)
- [Company data API reference](artifact/references/api-company.md)
- [Company registry API reference](artifact/references/api-registry.md)
- [Market analysis API reference](artifact/references/api-market.md)
- [Account API reference](artifact/references/api-account.md)
- [Device registration and account recovery guidance](artifact/references/auto-register.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown tables and concise textual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZLBX_API_KEY. Data queries may consume account credits.]

## Skill Version(s):

2.0.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
