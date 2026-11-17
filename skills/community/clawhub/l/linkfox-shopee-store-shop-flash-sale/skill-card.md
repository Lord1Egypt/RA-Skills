## Description:

Helps agents manage Shopee Shop Flash Sale campaigns for authorized stores, including time-slot lookup, campaign creation, listing, item management, updates, and deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace operators and their agents use this skill to operate Shopee Shop Flash Sale workflows for authorized stores. It supports reading available sale slots and campaign data, creating or changing flash sale events, managing items, deleting campaigns or items, and resolving LinkFox authentication or billing setup issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act on store authority and account credentials while creating, updating, or deleting Shopee flash sale campaigns and items.

Mitigation: Install and run it only in a controlled environment, and require explicit human confirmation before create, update, or delete operations.

Risk: LinkFox endpoint environment variables can redirect API traffic if set to untrusted destinations.

Mitigation: Keep LINKFOX_* endpoint variables unset unless the destination is trusted and expected for the current deployment.

Risk: Saved LinkFox response files may contain sensitive merchant or campaign data.

Mitigation: Treat saved linkfox response files as sensitive merchant data and restrict access to the workspace and session output directories.

Risk: The onboarding flow can create payment orders for billing remediation.

Mitigation: Require explicit human confirmation before payment-order commands and avoid unattended order creation or polling.

Risk: Workspace paths and SESSION_ID influence where response files are grouped and saved.

Mitigation: Run the skill from trusted workspaces and avoid attacker-controlled SESSION_ID or workspace path values.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-shop-flash-sale)
- [Publisher profile](https://clawhub.ai/user/linkfox-ai)
- [Shopee Shop Flash Sale API index](https://open.shopee.com/documents/v2/v2.shop_flash_sale.get_time_slot_id?module=123&type=1)
- [API field reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; API responses are JSON saved to session data files and printed or summarized on stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a LinkFox API key and the linkfox-shopee-store-auth dependency; saved responses may contain merchant data and should be treated as sensitive.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
