## Description: <br>
Queries and analyzes Amazon Brand Analytics search term data across 15 marketplaces with nearly three years of weekly data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and e-commerce analysts use this skill to query ABA search term reports, identify keyword trends, inspect click and conversion share, and generate tabular search-term analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API key and may operate on sensitive Amazon seller report workflows. <br>
Mitigation: Use only in environments where LinkFox is trusted for this data, scope credential access carefully, and avoid sensitive seller accounts unless approved by the data owner. <br>
Risk: The artifact instructs the agent to send feedback telemetry to a separate LinkFox API without interrupting the user flow. <br>
Mitigation: Review what the Feedback API transmits before deployment and disable or restrict feedback reporting if it is not acceptable under the user's data policy. <br>


## Reference(s): <br>
- [ABA Intelligent Query API Reference](artifact/references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-aba-data-explorer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and concise guidance, with optional shell commands or JSON API parameters.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CSV download links when requested and available from the API.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
