## Description:

Temu 全球站电商促销 API，经 LinkFox 网关转发 Partner Global Promotion / 促销活动 相关 bg/temu 接口（活动创建、报名、查询、优惠券/秒杀等，接口将按 Partner 文档逐条接入）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and developers use this skill to query Temu Global promotion activity data, find eligible goods, enroll goods in promotion activities, check operation results, update enrolled promotion goods, and download signed files through LinkFox gateway scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox API keys and Temu seller access tokens, including optional persistent local token storage.

Mitigation: Use a private workspace, restrict file permissions on token stores, avoid pasting credentials into shared logs, and delete or rotate stored tokens when no longer needed.

Risk: The generic proxy and file-download helpers can send broad Temu API requests beyond the six promotion-specific wrappers.

Mitigation: Review the requested API type, gateway endpoint environment variables, and request payload before execution; prefer the promotion-specific scripts for routine operations.

Risk: Promotion enrollment and update operations can affect live seller campaigns, including price, quantity, SKU participation, or deactivation.

Mitigation: Require explicit user confirmation for campaign-changing actions and verify activity IDs, goods IDs, SKU IDs, prices, quantities, and operateType values before running scripts.

Risk: Full API responses are written to local disk and may contain seller, product, campaign, or account data.

Mitigation: Avoid shared workspaces for outputs, inspect saved files before sharing, and remove session data that is no longer needed.

Risk: Evidence security verdict is suspicious because the skill handles credentials, payments or billing flows, broad proxying, and persistent storage.

Mitigation: Follow the server security guidance: review endpoint overrides, protect token storage, and require confirmation before billing, payment, or promotion-deactivation actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-promotion-global)
- [API Reference](references/api.md)
- [Temu Access Token Authorization](references/access-token.md)
- [Partner Global Promotion Catalog](references/partner-global-catalog.md)
- [Promotion API Index](references/apis/README.md)
- [LinkFox Onboarding](references/onboarding.md)
- [Temu Partner Global Documentation](https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896)
- [Temu Global OpenAPI Router](https://openapi-b-global.temu.com/openapi/router)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses saved to local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts write full API responses under a local linkfox session data directory and may print either full JSON or a summary depending on response size and inline mode.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
