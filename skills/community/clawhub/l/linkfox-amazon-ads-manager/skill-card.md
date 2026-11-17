## Description:

亚马逊广告（Amazon Ads）管理技能，覆盖 SP/SB/SD 的查询与创建/修改。Sponsored Brands 同时支持 V3 Legacy 与 V4：新活动、多 Ad Group、Ad/Creative 默认走 V4，历史 Legacy 可显式走 V3，Keyword/Target 按 Campaign 结构通过版本化脚本调用 Amazon 共享 targeting 资源；禁止 V4 失败后自动回落 V3，禁止用 V3 静默截断多 Ad Group 数据。适用于查询、创建、调价、改预算、改状态及管理 SP/SB/SD 广告。本技能依赖 linkfox-amazon-ads-auth；不覆盖 Sponsored Television / DSP。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon Ads operators and developers use this skill to query, create, and update Sponsored Products, Sponsored Brands, and Sponsored Display advertising entities through LinkFox-managed Amazon Ads access. It is suited to campaign, ad group, keyword, target, product ad, creative, budget, bid, and status management, with user confirmation expected for spend-impacting changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query and change Amazon Ads entities, including bids, budgets, and status.

Mitigation: Confirm the selected account, region, entity scope, and spend-impacting changes before running create or update operations.

Risk: Credential handling and endpoint overrides can expose API keys, SMS codes, or route requests to an untrusted destination.

Mitigation: Keep LINKFOX_TOOL_GATEWAY and related overrides unset unless the destination is trusted, and avoid placing API keys or SMS codes in transcripts or logs.

Risk: Full API responses are persisted locally and may contain sensitive account or advertising data.

Mitigation: Keep the linkfox output directory out of source control and delete retained response files when they are no longer needed.

Risk: Account and payment flows may present billing decisions outside normal ad-management work.

Mitigation: Review payment prompts separately and require explicit user approval before starting or changing a paid plan.

Risk: Automatic external feedback reporting may disclose operational context if sensitive details are included.

Mitigation: Do not include secrets, account identifiers, or sensitive campaign details in feedback content.

## Reference(s):

- [Amazon Ads Manager Skill Source](SKILL.md)
- [Amazon Ads API Overview](references/api.md)
- [Sponsored Products API Reference](references/api/sp.md)
- [Sponsored Brands API Reference](references/api/sb.md)
- [Sponsored Brands V3 Reference](references/api/sb-v3.md)
- [Sponsored Brands V4 Reference](references/api/sb-v4.md)
- [Sponsored Brands V3 and V4 Coexistence](references/api/sb-coexistence.md)
- [Sponsored Display API Reference](references/api/sd.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-ads-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are saved locally under a linkfox data directory; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
