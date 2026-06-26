## Description: <br>
Temu Price EU helps agents work with Temu Europe price-management APIs through LinkFox, including price-order queries, batch SKU base-price changes, and recommended supplier or base price lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and developers use this skill to query and update Temu EU product pricing through documented LinkFox gateway scripts and API references. It is intended for workflows that need Temu access tokens, LinkFox credentials, and careful review of live price-change requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Temu seller credentials and LinkFox tokens for live pricing operations. <br>
Mitigation: Install only when the publisher and LinkFox are trusted, pass short-lived tokens only when needed, and avoid saving production tokens locally. <br>
Risk: The skill includes bulk SKU base-price change workflows that can affect live product pricing. <br>
Mitigation: Manually review every bulk price-change payload, including goods IDs, SKU IDs, currency, and amount, before execution. <br>
Risk: Token retrieval and listing utilities can expose sensitive credential context in logs or shared environments. <br>
Mitigation: Do not run token retrieval or listing utilities in logged, shared, or untrusted environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/linkfox-ai/linkfox-temu-price-eu) <br>
- [API reference](references/api.md) <br>
- [Access token guidance](references/access-token.md) <br>
- [Partner EU catalog](references/partner-eu-catalog.md) <br>
- [Interface document index](references/apis/README.md) <br>
- [Temu Partner EU documentation](https://partner-eu.temu.com/documentation?menu_code=dfff38c23adf498d8a7cd55052bd3648) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with Python command examples and JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include live API request payloads and commands that require LinkFox and Temu credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
