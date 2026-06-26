## Description: <br>
Temu Price US helps agents query and update Temu US product pricing through LinkFox gateway scripts for price orders, SKU base-price changes, and recommended price estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and developers use this skill to inspect Temu US pricing records, estimate recommended supply prices, and prepare SKU base-price changes through documented Partner US price APIs. <br>

### Deployment Geography for Use: <br>
United States marketplace <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use stored Temu seller credentials and a LinkFox API token to make live pricing changes. <br>
Mitigation: Use least-privilege or short-lived tokens where possible, protect the local token store, and review every price-change payload before execution. <br>
Risk: Broad proxy and file-download utilities extend beyond the four scoped US price API wrappers. <br>
Mitigation: Remove or ignore the generic proxy and file-download scripts when only the US price APIs are needed. <br>
Risk: Raw access tokens may be supplied in command JSON or saved locally. <br>
Mitigation: Avoid printing raw tokens, prefer masked listings, restrict local file permissions, and rotate tokens after exposure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-temu-price-us) <br>
- [Publisher Profile](https://clawhub.ai/user/linkfox-ai) <br>
- [API Reference](references/api.md) <br>
- [Temu Access Token Guide](references/access-token.md) <br>
- [Partner US Price Catalog](references/partner-us-catalog.md) <br>
- [Price API Index](references/apis/README.md) <br>
- [Temu Partner US Documentation](https://partner-us.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or relay API response JSON from LinkFox and Temu when scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
