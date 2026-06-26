## Description: <br>
Provides Temu Global fulfillment and shipping API guidance and scripts for Buy-Shipping labels, cooperative warehouse fulfillment, self-fulfilled shipments, and tracking across 23 interfaces, excluding Scan Form. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and commerce operations teams use this skill to prepare and run Temu Global fulfillment workflows, including shipment creation, label retrieval, pickup reservation, cooperative warehouse fulfillment, seller-managed shipment confirmation, and logistics tracking. <br>

### Deployment Geography for Use: <br>
Global, excluding US/EU-specific Temu fulfillment workflows covered by separate skills. <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles powerful Temu and LinkFox credentials for live store fulfillment actions. <br>
Mitigation: Use only accounts authorized for the intended store, review each generated request before execution, and avoid pasting credentials into shared transcripts. <br>
Risk: The skill can create shipments, confirm fulfillment, cancel pickups, and call generic Temu API types. <br>
Mitigation: Require human approval before running shipment-changing commands and validate order, package, warehouse, carrier, and pickup identifiers against the source order system. <br>
Risk: Saved Temu access tokens may be stored locally in plaintext. <br>
Mitigation: Prefer short-lived manual token use when possible; if tokens are saved, restrict filesystem permissions, avoid synced directories, and rotate tokens after exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-temu-fulfillment-global) <br>
- [API reference](references/api.md) <br>
- [Access token guide](references/access-token.md) <br>
- [Partner Global catalog](references/partner-global-catalog.md) <br>
- [Fulfillment API index](references/apis/README.md) <br>
- [Temu Partner Global documentation](https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce live API call commands that require LinkFox and Temu credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
