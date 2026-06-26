## Description: <br>
Research dropshipping products and stores using TikTok and Facebook ad signals, product detail, and store intelligence from PipiAds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanyanggod](https://clawhub.ai/user/fanyanggod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and commerce operators use this skill to research dropshipping products, ad creatives, stores, and competitor patterns using PipiAds data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local MCP server uses the user's PipiAds/PipiSpy API key. <br>
Mitigation: Store PIPIADS_API_KEY as a secret environment variable, avoid sharing logs or configuration that expose it, and rotate the key if it is disclosed. <br>
Risk: The skill installs a pinned npm package that runs locally as an MCP server. <br>
Mitigation: Verify the pinned pipiads-mcp-server package and version before installation, and install it only in environments where the package is trusted. <br>
Risk: PipiAds API calls can consume paid account credits. <br>
Mitigation: Use tightly scoped searches, monitor credit usage and billing, and avoid broad exploratory queries unless the cost is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fanyanggod/pipiads-dropshipping-product-research) <br>
- [PipiAds homepage](https://www.pipiads.com) <br>
- [PipiSpy account and API key portal](https://www.pipispy.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research guidance with setup commands and API-derived findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local PipiAds MCP server and the user's PIPIADS_API_KEY; API calls may consume account credits.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
