## Description: <br>
Temu Price Global helps agents use LinkFox gateway scripts and reference docs for Temu Global price and supply-price APIs, including price-order queries, recommended prices, SKU supply-price lists, and batch SKU price changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, ecommerce operators, and agent builders use this skill to prepare authenticated Temu Global pricing API calls through LinkFox for supply-price lookup, recommended-price review, price-order inspection, and controlled SKU price updates. <br>

### Deployment Geography for Use: <br>
Global for Temu Global workflows, excluding the dedicated US and EU Temu site skills. <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires LinkFox and Temu seller credentials, and helper scripts can save Temu access tokens locally. <br>
Mitigation: Use least-privilege dedicated Temu tokens, avoid saving production tokens locally when possible, protect command history and logs, and remove stored tokens when no longer needed. <br>
Risk: The artifact includes generic proxy and file-download helpers beyond the narrow pricing workflow. <br>
Mitigation: Use only the pricing-specific scripts required for the task, and remove or avoid generic proxy and download helpers when they are not needed. <br>
Risk: The batch price-change endpoint can modify SKU supply prices. <br>
Mitigation: Require explicit human approval before any batch price change and verify request payloads and post-change query results. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/linkfox-ai/linkfox-temu-price-global) <br>
- [API reference](references/api.md) <br>
- [Access token authorization](references/access-token.md) <br>
- [Authorization flow](references/authorization-flow.md) <br>
- [Partner Global catalog](references/partner-global-catalog.md) <br>
- [Endpoint documentation index](references/apis/README.md) <br>
- [Temu Partner Global documentation](https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request and response JSON, credential setup steps, and operational cautions for pricing changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
