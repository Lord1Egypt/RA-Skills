## Description:

Provides Shopee SBS warehouse and inventory query workflows for bound warehouses, current inventory, expiry reports, stock aging, and stock movement through LinkFox's Shopee integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Shopee sellers, store operators, and agents use this skill to inspect authorized SBS warehouse bindings, inventory levels, expiry status, stock aging, and stock movement history for operational reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires LinkFox/Shopee account access through API keys and authorized store identifiers.

Mitigation: Use only intended business accounts, avoid exposing API keys in shared shell profiles, and rotate keys if they are copied into an unsafe location.

Risk: Onboarding helpers can support billing and payment order flows.

Mitigation: Run payment or order commands only after explicit user confirmation that credits should be purchased.

Risk: LINKFOX_* endpoint environment variables can alter which service endpoints receive requests.

Mitigation: Review endpoint-related environment variables before use and restrict them to trusted LinkFox endpoints.

Risk: Saved response files may contain store inventory or other sensitive business data.

Mitigation: Store workspaces securely and clean up generated linkfox response files when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-sbs)
- [SBS API reference](references/api.md)
- [Bound warehouse info reference](references/apis/get-bound-whs-info.md)
- [Current inventory reference](references/apis/get-current-inventory.md)
- [Expiry report reference](references/apis/get-expiry-report.md)
- [Stock aging reference](references/apis/get-stock-aging.md)
- [Stock movement reference](references/apis/get-stock-movement.md)
- [Shopee Open Platform SBS get_bound_whs_info](https://open.shopee.com/documents/v2/v2.sbs.get_bound_whs_info?module=124&type=1)
- [Shopee Open Platform SBS get_current_inventory](https://open.shopee.com/documents/v2/v2.sbs.get_current_inventory?module=124&type=1)
- [Shopee Open Platform SBS get_expiry_report](https://open.shopee.com/documents/v2/v2.sbs.get_expiry_report?module=124&type=1)
- [Shopee Open Platform SBS get_stock_aging](https://open.shopee.com/documents/v2/v2.sbs.get_stock_aging?module=124&type=1)
- [Shopee Open Platform SBS get_stock_movement](https://open.shopee.com/documents/v2/v2.sbs.get_stock_movement?module=124&type=1)

## Skill Output:

**Output Type(s):** [text, json, files, shell commands, configuration, guidance]

**Output Format:** [JSON responses saved to session files, stdout JSON or summaries, and Markdown guidance with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are retained under linkfox session data; large responses print summaries unless inline output is requested.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
