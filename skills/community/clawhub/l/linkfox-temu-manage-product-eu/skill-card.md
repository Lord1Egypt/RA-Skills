## Description:

This skill helps agents manage Temu Partner EU catalog products through LinkFox, including product and SKU lookup, stock edits, publish or sale status changes, partial or full product updates, deletion, compliance edits, category checks, property templates, external codes, and video cover retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce operators, developers, and external sellers use this skill with an agent to inspect and manage live Temu EU product catalog records through LinkFox and Temu access tokens. It is intended for product operations such as finding goods, editing inventory and listing details, changing sale status, and checking compliance or category data.

### Deployment Geography for Use:

Europe (Temu Partner EU)

## Known Risks and Mitigations:

Risk: The skill can mutate live Temu EU catalog data, including product content, inventory, sale status, compliance information, and deletion.

Mitigation: Confirm the store, product IDs, SKU IDs, and intended operation before running mutation scripts; require deliberate approval for update, delete, stock, sale status, and compliance actions.

Risk: The skill handles LinkFox API keys and Temu merchant access tokens, including optional local token persistence.

Mitigation: Use minimally scoped Temu permissions, avoid printing or logging tokens, protect any local token file with owner-only permissions, and rotate expired or overbroad tokens.

Risk: The server security evidence flags the release for review because credentials, billing concerns, and local persistence are broad for a live business workflow.

Mitigation: Install only when LinkFox is trusted with Temu merchant data, review security guidance before use, and treat billing or payment-related flows as separate actions requiring explicit approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-manage-product-eu)
- [API reference](references/api.md)
- [Partner EU manage product catalog](references/partner-eu-catalog.md)
- [Temu access token authorization](references/access-token.md)
- [Per-interface API documents](references/apis/README.md)
- [Temu Partner EU documentation](https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses printed to stdout or saved as local files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Large API responses are summarized in stdout while full JSON responses are saved under a local linkfox data directory.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
