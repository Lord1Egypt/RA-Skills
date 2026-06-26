## Description: <br>
Searches Mysteel commodity industry information for steel, non-ferrous metals, energy chemicals, market alerts, policy changes, company updates, price movement analysis, and supply-demand events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyb92](https://clawhub.ai/user/wyb92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Commodity-market analysts, researchers, and business users use this skill to query Mysteel for industry news, policy updates, company developments, price movement explanations, and supply-demand events. Developers can run the included command-line script to submit a query and receive structured Mysteel API results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads an API token from references/api_key.md for requests to Mysteel. <br>
Mitigation: Use a dedicated Mysteel key, keep references/api_key.md private, and do not commit the key file. <br>
Risk: Search terms are sent to Mysteel's external API. <br>
Mitigation: Avoid submitting confidential, regulated, or sensitive business information as query text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wyb92/mysteel-infosearch) <br>
- [Mysteel API Reference](references/api_reference.md) <br>
- [Mysteel AI Search API endpoint](https://mcp.mysteel.com/mcp/info/ai-search/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance and command-line JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The --raw option prints the unmodified JSON response from Mysteel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
