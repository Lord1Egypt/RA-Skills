## Description: <br>
Screens and ranks Amazon category markets using SellerSprite market-research data, including market size, competition, seller structure, concentration, pricing, ratings, margin, and new-product signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, marketplace researchers, and product-sourcing teams use this skill to identify and compare Amazon category market opportunities. It helps filter category-level markets by demand, revenue, concentration, seller mix, fulfillment mix, price, rating, margin, and new-product indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credentialed requests send Amazon market-research filters and category details to LinkFox/SellerSprite. <br>
Mitigation: Use only with an approved LINKFOXAGENT_API_KEY and avoid submitting sensitive business strategy details beyond the filters needed for the query. <br>
Risk: The skill documentation asks agents to auto-report feedback through a separate Feedback API without explicit user interruption. <br>
Mitigation: Prefer a version or operating policy that asks before sending feedback or conversation-derived content to the Feedback API. <br>
Risk: The security verdict is suspicious because the skill can route broad research requests and feedback outside the local agent environment. <br>
Mitigation: Review the skill before installing, confirm external data-sharing expectations, and monitor outbound API use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-sellersprite-market-research) <br>
- [SellerSprite market-research API reference](references/api.md) <br>
- [SellerSprite market-research script](scripts/sellersprite_market_research.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON parameters, shell command examples, and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and sends Amazon market-research filters to LinkFox/SellerSprite services.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
