## Description: <br>
Amazon Search helps agents simulate live Amazon storefront searches and report search result positions, sponsored listings, prices, ratings, brands, delivery details, and related SERP data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators, marketplace analysts, and selling teams use this skill to inspect current Amazon search results for a keyword across supported marketplaces. It is suited for rank checks, competitor discovery, price comparison, sponsored product review, new-product monitoring, and device or location-specific SERP analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API key and sends Amazon search queries plus optional delivery ZIP or postal codes to the LinkFox gateway. <br>
Mitigation: Use it only in environments where LinkFox is trusted, store the API key in the environment, rotate credentials when needed, and avoid sending sensitive location or business data unless necessary. <br>
Risk: The artifact describes automatic feedback reporting that can send conversation-derived details to a separate LinkFox feedback service. <br>
Mitigation: Disable feedback reporting or send it only after explicit user approval, and omit details that are not required to describe the issue. <br>


## Reference(s): <br>
- [Amazon Search API Reference](references/api.md) <br>
- [Amazon Search on ClawHub](https://clawhub.ai/linkfox-ai/linkfox-amazon-search) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples, shell command examples, and tabular search-result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a LinkFox API that returns JSON search results containing product listings, prices, ratings, sponsored flags, positions, images, links, and delivery fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
