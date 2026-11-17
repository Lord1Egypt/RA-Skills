## Description:

Helps agents generate native WeChat mini-program storefront code and integration guidance for Ushopun commerce backends using the bundled Ushopun V2 OpenAPI reference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urselect](https://clawhub.ai/user/urselect)

### License/Terms of Use:

MIT

## Use Case:

Developers and external builders use this skill to create Ushopun-backed WeChat mini-program storefronts covering product discovery, cart, checkout, orders, account pages, and related commerce flows. It also guides API wiring for tenant-specific Ushopun deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to work with a tenant-level Ushopun ApiToken for validation or live testing.

Mitigation: Use the bundled OpenAPI file first; only provide short-lived, least-privilege test credentials for explicit live testing, and never place production tokens in generated source.

Risk: Generated commerce flows may submit orders, start payments, perform wallet recharge or withdrawal, upgrade agent status, post content, or send messages.

Mitigation: Require manual review and explicit approval before generated code performs financial, account-changing, order-changing, content-posting, or messaging actions.

## Reference(s):

- [Server-resolved source repository](https://github.com/urselect/miniprogram-mall-ushopun-skill)
- [ClawHub skill page](https://clawhub.ai/urselect/skills/miniprogram-mall-ushopun-skill)
- [Ushopun V2 OpenAPI reference](artifact/openapi.json)
- [Ushopun development endpoint](https://dev.ushopun.com)

## Skill Output:

**Output Type(s):** [Code, Markdown, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown with code snippets and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce WeChat mini-program page files, API wrapper patterns, endpoint constants, and integration checklists.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
