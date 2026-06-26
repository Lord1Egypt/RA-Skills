## Description: <br>
Food, recipe, brewery, and nutrition lookup guidance for Pilot Protocol service agents backed by OpenFoodFacts, TheCocktailDB, TheMealDB, Fruityvice, and Open Brewery DB. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to discover Pilot Protocol food-related service agents, inspect each agent's filter contract, and query product, recipe, ingredient, brewery, and reference nutrition data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Barcode, ingredient, location, recipe, and nutrition queries may be handled as external network traffic through Pilot Protocol service agents. <br>
Mitigation: Install only when the Pilot Protocol daemon and pilotctl setup are trusted, and avoid sending private health, personal, or secret information. <br>
Risk: Food catalogs, agent availability, and nutrition facts are reference data and may be incomplete, stale, or unsuitable for medical nutrition advice. <br>
Mitigation: Use list-agents and /help to verify current agent contracts, and route medical nutrition questions to an appropriate health-specific workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-service-agents-food) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot skills catalog](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent replies may arrive asynchronously through pilotctl inbox; summary and free-text queries can return generated prose.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
