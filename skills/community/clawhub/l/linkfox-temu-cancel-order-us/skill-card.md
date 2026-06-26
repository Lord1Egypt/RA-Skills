## Description: <br>
Helps an agent guide and run Temu US buyer and seller order-cancellation API workflows through the LinkFox gateway, including after-sales cancel list and agree, cancel appeal, and out-of-stock cancel operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Temu sellers, operations teams, and developers use this skill to prepare cancel-order API payloads, choose the correct LinkFox helper script, and manage buyer or seller cancellation flows for US orders. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes broad gateway, file-download, and token-handling capabilities for live Temu seller/API authority. <br>
Mitigation: Install only when the LinkFox gateway is trusted, prefer the dedicated cancel-order scripts over the generic proxy, and avoid the file-download helper unless it is specifically needed. <br>
Risk: LinkFox and Temu credentials are sensitive and may be handled locally by helper scripts. <br>
Mitigation: Store Temu tokens in a proper secret manager or with tightly restricted local file permissions, and avoid unmasked token listing. <br>
Risk: Order-cancellation actions can affect live Temu US orders. <br>
Mitigation: Review order identifiers, request payloads, and API results before executing cancellation or appeal operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-temu-cancel-order-us) <br>
- [API Reference](references/api.md) <br>
- [Temu Access Token Authorization](references/access-token.md) <br>
- [Partner US Cancel Order Catalog](references/partner-us-catalog.md) <br>
- [Cancel Order API Index](references/apis/README.md) <br>
- [Temu Partner US Documentation](https://partner-us.temu.com/documentation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke helper scripts that return parsed JSON from LinkFox and Temu APIs when credentials are supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
