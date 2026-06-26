## Description: <br>
Temu Fulfillment EU helps agents work with Temu EU fulfillment workflows, including buy-shipping labels, cooperative warehouse fulfillment, self-fulfilled shipment updates, tracking, scan forms, pickup reservations, and self-delivery POD upload and audit flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and developers use this skill to automate Temu EU fulfillment and shipping tasks through documented API wrappers. It supports order-shipping workflows such as label purchase, warehouse fulfillment submit or cancel, tracking lookup, shipment confirmation, pickup reservation, and POD handling. <br>

### Deployment Geography for Use: <br>
Europe (Temu EU fulfillment workflows) <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live fulfillment actions that affect shipments, pickup reservations, warehouse fulfillment, and POD workflows. <br>
Mitigation: Require human confirmation before shipment creation, shipment confirmation, pickup cancellation, warehouse fulfillment cancellation, or other state-changing operations. <br>
Risk: The skill requires sensitive LinkFox and Temu credentials, and its token-store helper writes Temu access tokens to a local plaintext JSON file by default. <br>
Mitigation: Use least-privilege and purpose-specific tokens, avoid sharing secrets in chat or shell history, restrict file permissions, and prefer a secure secret manager or protected token-store path. <br>
Risk: Server security evidence marks the release suspicious because it changes live shipping operations and uses weak local token safeguards. <br>
Mitigation: Install only when the publisher is trusted and the operator needs live Temu EU fulfillment automation; review requested actions and inputs before execution. <br>


## Reference(s): <br>
- [Skill Overview](artifact/SKILL.md) <br>
- [API Reference](artifact/references/api.md) <br>
- [Access Token Guide](artifact/references/access-token.md) <br>
- [Authorization Flow](artifact/references/authorization-flow.md) <br>
- [Partner EU Fulfillment Catalog](artifact/references/partner-eu-catalog.md) <br>
- [API Documentation Index](artifact/references/apis/README.md) <br>
- [Temu Partner EU Documentation](https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-temu-fulfillment-eu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls, JSON] <br>
**Output Format:** [Markdown guidance with Python shell commands and JSON request or response examples; live API calls return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LinkFox and Temu credentials for live fulfillment operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
