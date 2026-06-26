## Description: <br>
Guides agents to query LinkFox SIF data for Amazon ASIN traffic keywords, including organic and ad rankings, search volume, traffic share, conversion markers, and week, month, or latest-period windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and ecommerce analysts use this skill to reverse-look up the keywords driving traffic to a single ASIN and inspect ranking, advertising, search-volume, and conversion indicators. Agents can use it to make authenticated LinkFox API calls and present the returned data in clear tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ASIN and keyword research queries are sent to LinkFox using a LinkFox API key. <br>
Mitigation: Use only when the user is comfortable sending the query data to LinkFox, and avoid including private business context unless necessary. <br>
Risk: The skill instructs agents to silently submit user feedback and intent details to a separate LinkFox endpoint. <br>
Mitigation: Disable feedback submissions or require explicit user consent before sending comments, intent details, or other user-provided context. <br>


## Reference(s): <br>
- [SIF ASIN Keywords API reference](references/api.md) <br>
- [LinkFox SIF ASIN keywords endpoint](https://tool-gateway.linkfox.com/sif/asinKeywords) <br>
- [ClawHub release page](https://clawhub.ai/linkfox-ai/linkfox-sif-asin-keywords) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and queries one ASIN per request.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
