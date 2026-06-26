## Description: <br>
Explore and analyze Amazon e-commerce data at scale, including product search, category browsing, product details, best sellers, deals, seller intelligence, influencer storefronts, reviews, and ASIN/GTIN conversion across 24 Amazon marketplaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and analysts use this skill to query KeyAPI's Amazon MCP service for product, seller, deal, review, and influencer storefront research across supported Amazon marketplaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tokens or cached Amazon research results may persist locally if the runner creates a .env file or writes .keyapi-cache files. <br>
Mitigation: Prefer setting KEYAPI_TOKEN as an environment variable, review or delete any .env file created by the runner, and use --no-cache or remove .keyapi-cache when results are sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lycici/keyapi-amazon-ecommerce) <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI Amazon MCP endpoint](https://mcp.keyapi.ai/amazon/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KEYAPI_TOKEN and Node.js; can cache API responses locally under .keyapi-cache.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
