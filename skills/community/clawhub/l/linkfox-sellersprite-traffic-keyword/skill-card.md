## Description: <br>
Queries SellerSprite traffic keyword data for an Amazon ASIN, including traffic sources, traffic share categories, conversion types, organic rank, ad rank, historical months, and sorting options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, ecommerce operators, and agents use this skill to look up traffic keyword lists for Amazon ASINs and present keyword, organic rank, ad rank, traffic share, conversion type, and pagination details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox/SellerSprite API key to call an external keyword lookup service. <br>
Mitigation: Store LINKFOXAGENT_API_KEY as a managed secret, limit who can run the skill, and rotate or revoke the key if access changes. <br>
Risk: The skill includes instructions for agents to send broad feedback to a separate LinkFox endpoint without clear user consent. <br>
Mitigation: Disable or remove the feedback workflow unless the operator explicitly wants external feedback submission and users understand what may be sent. <br>


## Reference(s): <br>
- [API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-sellersprite-traffic-keyword) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls an external SellerSprite traffic keyword API and requires LINKFOXAGENT_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
