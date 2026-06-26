## Description: <br>
Helps agents use LinkFox scripts and reference docs to call Temu Global returns, refunds, and after-sales APIs for return requests, refund data, after-sales order lookup, return logistics, labels, carriers, and signatures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Temu sellers, operators, and developers use this skill to query and manage Temu Global returns, refunds, after-sales records, return logistics, labels, carriers, and related token setup through LinkFox gateway scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles LinkFox API keys and Temu merchant access tokens, including optional local storage of reusable Temu tokens. <br>
Mitigation: Use a protected single-user machine or a secret manager, prefer short-lived credentials when possible, avoid printing tokens, and rotate any credential that was logged or stored insecurely. <br>
Risk: Generic proxy scripts can call Temu APIs beyond the documented returns and refunds workflows. <br>
Mitigation: Review the requested API type and parameters before execution, restrict credentials to the minimum needed permissions, and audit usage against expected returns and refunds tasks. <br>
Risk: Returns and refunds workflows can expose merchant, order, after-sales, logistics, and refund data. <br>
Mitigation: Run only in trusted environments, limit output sharing, and avoid pasting customer or merchant data into unrelated conversations or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-temu-returns-refunds-global) <br>
- [API reference](references/api.md) <br>
- [Access token guide](references/access-token.md) <br>
- [Partner Global catalog](references/partner-global-catalog.md) <br>
- [Returns and refunds API index](references/apis/README.md) <br>
- [Temu Global OpenAPI router](https://openapi-b-global.temu.com/openapi/router) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and Python shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts may return gateway JSON, parsed Temu response bodies, or local token-store status.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
