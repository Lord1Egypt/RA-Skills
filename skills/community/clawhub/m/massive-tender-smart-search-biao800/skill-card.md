## Description:

Searches tender and award notices using complex criteria such as multiple keywords, excluded terms, and amount ranges, then presents filtered results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pkuycl](https://clawhub.ai/user/pkuycl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business analysts use this skill to search tender and award notices and request selected company, market, and registry information. It combines user-specified filters and summarizes returned results with relevant source and completeness limits.

### Deployment Geography for Use:

Global (focus: Chinese tender and company data)

## Known Risks and Mitigations:

Risk: Automatic signup sends device characteristics, including a hashed MAC address, for device-based deduplication; the supplied privacy wording may understate this identification risk.

Mitigation: Before installation or automatic signup, clearly disclose the device data sent and obtain user consent. Users can configure their own API key to skip automatic registration.

Risk: Update acknowledgments and credential handling may not be sufficiently scoped, and saved API keys or temporary login links could be exposed.

Mitigation: Use a fixed, validated same-origin acknowledgment endpoint and protect saved keys and temporary login links.

Risk: Selected search criteria are sent to Zhiliaobiaoxun, and successful paid lookups consume credits.

Mitigation: Tell users which criteria will be sent and the applicable lookup cost before making paid queries; limit calls to the user's requested scope.

## Reference(s):

- [Tender search API reference](artifact/references/api-search.md)
- [Company information API reference](artifact/references/api-company.md)
- [Market analysis API reference](artifact/references/api-market.md)
- [Company registry API reference](artifact/references/api-registry.md)
- [Account API reference](artifact/references/api-account.md)
- [Account setup and automatic registration guide](artifact/references/auto-register.md)
- [ClawHub release page](https://clawhub.ai/pkuycl/skills/massive-tender-smart-search-biao800)
- [Zhiliaobiaoxun API documentation](https://ai.zhiliaobiaoxun.com/docs/skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown summaries and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports returned search and business data with source, freshness, and completeness limits where available.]

## Skill Version(s):

1.0.11 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
