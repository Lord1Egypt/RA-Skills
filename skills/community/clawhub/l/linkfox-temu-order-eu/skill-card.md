## Description: <br>
Provides Temu EU order-management guidance, reference material, and scripts for LinkFox gateway access to Partner EU order APIs, including order lists, details, shipping information, amounts, combined shipments, customization data, and verification uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operations teams, and developers use this skill to query and manage Temu EU order workflows through LinkFox gateway scripts and API documentation. <br>

### Deployment Geography for Use: <br>
Europe <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Temu seller order data, shipping details, and reusable Temu or LinkFox credentials. <br>
Mitigation: Install only for agents and environments that are permitted to handle those data classes, and scope credentials to the minimum order workflow needed. <br>
Risk: The artifact includes utilities for storing Temu access tokens in a local plaintext token file. <br>
Mitigation: Prefer passing tokens only when needed, avoid local plaintext token storage where possible, and rotate any token that may have been exposed in logs or shell history. <br>
Risk: Generic proxy and file-download scripts provide broader access than a single order API workflow may require. <br>
Mitigation: Use the specific order scripts for routine tasks and reserve generic proxy or file-download scripts for cases where that broader access is intentionally required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-temu-order-eu) <br>
- [API reference](references/api.md) <br>
- [Temu access token guide](references/access-token.md) <br>
- [Partner EU catalog](references/partner-eu-catalog.md) <br>
- [Order API index](references/apis/README.md) <br>
- [Temu Partner EU documentation](https://partner-eu.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9) <br>
- [LinkFox Temu gateway](https://tool-gateway.linkfox.com/temu/proxy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include API request bodies, token-handling steps, and script invocation commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
