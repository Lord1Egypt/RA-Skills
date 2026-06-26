## Description: <br>
Helps agents search Amazon marketplaces by public image URL and return visually similar product listings with product metadata and optional Keepa enrichment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, researchers, and agents use this skill to find visually similar Amazon products from a public image URL across supported marketplaces for competitive analysis, sourcing alternatives, and product discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LinkFox receives submitted image URLs and search metadata when the search API is used. <br>
Mitigation: Use only public, non-sensitive image URLs; avoid private or signed URLs; and use a revocable API key. <br>
Risk: The skill instructs agents to report feedback and user context to a separate LinkFox feedback API without interrupting the user flow. <br>
Mitigation: Disable or override automatic feedback reporting unless the user explicitly agrees to send feedback content. <br>
Risk: The server security verdict is suspicious and says the release needs review. <br>
Mitigation: Review the skill before deployment and confirm that third-party API calls, credential handling, and feedback behavior match local policy. <br>


## Reference(s): <br>
- [API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-amazon-search-by-image) <br>
- [LinkFox Amazon image search API](https://tool-gateway.linkfox.com/amazon/searchByImage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown tables and JSON API responses, with optional shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a public image URL, a supported Amazon marketplace domain, and LINKFOXAGENT_API_KEY for direct API or script execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
