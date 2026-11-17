## Description:

Temu 美国站订单管理 API skill for routing Partner US order operations through the LinkFox gateway, including order lists, details, shipping information, order amounts, combined shipment groups, customization retrieval, and SN/IMEI verification upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Temu merchants, operators, and developers use this skill to inspect and manage US Partner order data through LinkFox, including order lookup, sensitive shipping-address retrieval, amount checks, combined-shipment discovery, customization files, and verification uploads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox and Temu merchant credentials.

Mitigation: Prefer storeKey-based token lookup over pasting access tokens into commands, avoid shared machines, and restrict who can read local token files.

Risk: The skill can retrieve customer shipping/contact data and order records, including decrypted shipping information.

Mitigation: Run it only in workspaces approved for customer data, limit use to necessary orders, and clean up saved response files after use.

Risk: Gateway endpoint override environment variables can redirect requests.

Mitigation: Review or restrict LINKFOX_TOOL_GATEWAY, TEMU_API_BASE_URL, and STORE_API_BASE_URL before execution.

Risk: Onboarding and package purchase flows may affect account or billing state.

Mitigation: Do not proceed with onboarding or paid package purchase flows unless the user explicitly requested them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-order-us)
- [API Reference](references/api.md)
- [Access Token Guide](references/access-token.md)
- [Authorization Flow](references/authorization-flow.md)
- [Partner US Order Catalog](references/partner-us-catalog.md)
- [Temu Partner US Documentation](https://partner-us.temu.com/documentation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON and shell command examples; scripts emit JSON responses or summaries and may save full response files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Handles LinkFox and Temu credentials, order records, customer shipping/contact data, customization files, and verification upload payloads.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
