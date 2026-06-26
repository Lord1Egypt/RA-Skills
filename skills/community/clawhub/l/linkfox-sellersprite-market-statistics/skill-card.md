## Description: <br>
Fetches SellerSprite node-level market statistics for Amazon categories, including top listing averages, pricing, BSR, sales, seller counts, and new-product indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, marketplace analysts, and developers use this skill to query Amazon category node statistics and assess market quality, competition, and new-product activity before product-sourcing decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses LINKFOXAGENT_API_KEY and sends category-statistics queries to LinkFox/SellerSprite. <br>
Mitigation: Install only if sharing those queries with LinkFox/SellerSprite is acceptable, and protect the API key as a sensitive credential. <br>
Risk: The skill directs automatic feedback reporting to LinkFox without clear user control during the workflow. <br>
Mitigation: Review the feedback behavior before deployment and avoid sending interaction summaries unless that data sharing is acceptable. <br>


## Reference(s): <br>
- [SellerSprite Market Statistics API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-sellersprite-market-statistics) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON API responses and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY for live API calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
