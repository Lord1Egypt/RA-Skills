## Description: <br>
Provides LinkFox-gateway scripts and references for managing Temu Partner US products across 24 bg.local and temu.local APIs, including product queries, edits, deletion, stock, sale status, compliance, and media workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Temu sellers, operators, and developers use this skill to query and change US Partner product listings through LinkFox-managed scripts and API references. It is intended for product-management tasks such as listing lookup, detail retrieval, updates, deletion, stock changes, sale-status changes, compliance edits, and token handling. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete Temu product listings, stock, sale status, and compliance data. <br>
Mitigation: Require explicit human confirmation before deletion, full update, stock, sale-status, or compliance changes. <br>
Risk: The skill requires sensitive LinkFox and Temu access tokens, and the artifact includes local token-store helpers. <br>
Mitigation: Treat tokens like passwords, avoid plaintext local token storage on shared or unmanaged machines, and do not print tokens into chats or logs. <br>
Risk: The generic proxy can provide broader API access than the US-only product-management workflow needs. <br>
Mitigation: Prefer the fixed us_manage_* scripts over the generic proxy unless broader API access is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-temu-manage-product-us) <br>
- [Temu Partner US Manage Product catalog](references/partner-us-catalog.md) <br>
- [LinkFox Temu Manage Product API reference](references/api.md) <br>
- [Temu accessToken authorization guide](references/access-token.md) <br>
- [Per-API reference index](references/apis/README.md) <br>
- [Temu Partner US Product > Manage Product documentation](https://partner-us.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON command examples and Python script invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a LinkFox API key and a Temu access token or stored storeKey; some scripts can perform product-management changes through the LinkFox gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
