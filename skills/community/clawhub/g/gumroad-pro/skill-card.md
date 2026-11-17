## Description:

Comprehensive Gumroad merchant management for Products, Sales, Licenses, Discounts, Payouts, and Webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdul-karim-mia](https://clawhub.ai/user/abdul-karim-mia)

### License/Terms of Use:

MIT

## Use Case:

Gumroad merchants and operators use this skill to manage products, sales, license keys, discounts, payouts, custom fields, and webhooks through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act with a live Gumroad merchant token.

Mitigation: Install only when the publisher is trusted, use a dedicated Gumroad token, and prefer GUMROAD_ACCESS_TOKEN over a generic API_KEY.

Risk: Refunds, deletions, license changes, custom-field changes, and shipping updates can affect live merchant operations.

Mitigation: Review target IDs, amounts, and customer context before execution, and require explicit user confirmation for high-impact actions.

Risk: Sales and shipping workflows can expose customer and fulfillment data.

Mitigation: Limit data shown in chat to what is needed for the task and avoid retaining customer, license, or shipping details outside the active session.

## Reference(s):

- [Gumroad Pro API Reference](references/api-reference.md)
- [Gumroad Pro Handler Guide](references/handler-guide.md)
- [Gumroad Pro UI Rendering](references/ui-rendering.md)
- [Gumroad Pro Changelog](references/changelog.md)
- [Gumroad Pro on ClawHub](https://clawhub.ai/abdul-karim-mia/skills/gumroad-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown, JSON command output, and interactive merchant-management responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a Gumroad merchant token provided through GUMROAD_ACCESS_TOKEN, with API_KEY accepted as a fallback.]

## Skill Version(s):

1.2.9 (source: package.json, _meta.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
