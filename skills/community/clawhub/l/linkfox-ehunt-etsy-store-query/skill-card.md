## Description: <br>
Guides an agent to query LinkFox/EHunt's `_ehunt_storeQuery` tool for Etsy shop research across sales, favorites, reviews, opening date, country, category, Raving status, and starred status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketplace researchers and ecommerce operators use this skill to find, filter, and compare Etsy stores with EHunt data. It is intended for store discovery and performance analysis when LinkFox/EHunt access is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API key and sends query parameters to the LinkFox/EHunt service. <br>
Mitigation: Store the API key only in a secure environment variable and avoid placing secrets or sensitive business strategy in search fields. <br>
Risk: The skill can activate for broad Etsy store research requests and may query a third-party data service. <br>
Mitigation: Confirm the intended query scope before invoking the tool for broad Etsy questions. <br>


## Reference(s): <br>
- [_ehunt_storeQuery API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-ehunt-etsy-store-query) <br>
- [LinkFox tool gateway](https://tool-gateway.linkfox.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with JSON request examples and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a LinkFox API key in `LINKFOXAGENT_API_KEY`; API responses contain Etsy store data returned by the upstream service.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
