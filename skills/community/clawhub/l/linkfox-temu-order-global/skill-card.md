## Description: <br>
Temu Order Global helps agents call LinkFox gateway scripts and documentation for nine Temu Global order-management APIs, including order lists, details, shipping information, amounts, combined shipments, customization, and verification uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and developers use this skill to query and manage Temu Global order data through LinkFox gateway scripts, including shipping details, order amounts, combined-shipment candidates, and SN/IMEI verification uploads. <br>

### Deployment Geography for Use: <br>
Global, for Temu Global order workflows; US and EU workflows are directed to separate skill variants. <br>

## Known Risks and Mitigations: <br>
Risk: Broad LinkFox gateway and Temu order API access can expose order-management actions beyond the immediate request. <br>
Mitigation: Install only when the LinkFox publisher is trusted, use least-privilege Temu tokens, and avoid the generic proxy for non-order calls. <br>
Risk: Temu access tokens may be stored in a local plaintext token file. <br>
Mitigation: Prefer a secure secret manager or hardened token file permissions, and avoid sharing token command output in logs or chats. <br>
Risk: Shipping addresses, decrypted contact details, signed files, and SN/IMEI values are sensitive customer data. <br>
Mitigation: Handle outputs as confidential customer data and limit retention, display, and downstream sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-temu-order-global) <br>
- [API reference](references/api.md) <br>
- [Temu access token authorization](references/access-token.md) <br>
- [Order API index](references/apis/README.md) <br>
- [Partner Global catalog](references/partner-global-catalog.md) <br>
- [Temu Partner Global documentation](https://partner-global.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON request/response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a LinkFox API key and a Temu access token or storeKey; scripts print JSON responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
