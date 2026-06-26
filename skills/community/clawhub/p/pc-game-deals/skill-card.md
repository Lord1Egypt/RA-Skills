## Description: <br>
Track PC game discounts across Steam, Epic Games, GOG, Humble Store, and 30+ stores via the CheapShark API for PC game deal lookups, sale checks, lowest-price requests, and price-alert guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pazzilivo](https://clawhub.ai/user/Pazzilivo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to find PC game discounts, inspect store-specific deals, compare current and historical prices, and locate CheapShark's web-based price-alert flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Game titles and deal queries may be sent to CheapShark over the network. <br>
Mitigation: Avoid entering private or sensitive search terms when using the lookup commands. <br>
Risk: The optional price-alert flow requires entering an email address on CheapShark's website. <br>
Mitigation: Use price alerts only when comfortable sharing an email address with CheapShark. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Pazzilivo/pc-game-deals) <br>
- [CheapShark Stores API](https://www.cheapshark.com/api/1.0/stores) <br>
- [CheapShark Website](https://www.cheapshark.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline bash commands and JSON-processing examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; sends game titles and deal queries to CheapShark over the network.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
