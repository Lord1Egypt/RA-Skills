## Description: <br>
Temu Order US helps agents work with Temu US order-management APIs through the LinkFox gateway, including order lists, order details, shipping information, decrypted shipping information, order amounts, combined-shipment groups, customization details, and SN or IMEI verification uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and developers use this skill to query and manage Temu US order data, inspect fulfillment and shipping details, reconcile order amounts, and upload required order verification values through LinkFox-mediated Temu APIs. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses live Temu seller credentials and customer order data. <br>
Mitigation: Install only from a trusted publisher, use least-privilege order-only tokens, and avoid pasting or logging tokens. <br>
Risk: The bundled helpers can store Temu access tokens in a local plaintext token file. <br>
Mitigation: Use a protected secret manager or tightly control the token-store path and file permissions. <br>
Risk: The skill includes a broad Temu proxy and helpers that can list saved tokens. <br>
Mitigation: Prefer the specific order-management scripts and avoid the generic proxy or raw token listing helpers unless necessary. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-temu-order-us) <br>
- [API Reference](references/api.md) <br>
- [Access Token Guide](references/access-token.md) <br>
- [Partner US Catalog](references/partner-us-catalog.md) <br>
- [Order API Index](references/apis/README.md) <br>
- [Temu Partner US Documentation](https://partner-us.temu.com/documentation) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request or response payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LinkFox authentication and a Temu seller access token or configured store key.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
