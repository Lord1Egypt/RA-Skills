## Description: <br>
Hokkaido travel companion protocol for collecting, verifying, storing, and reusing travel knowledge with a local vault plus live search for restaurants, transport, weather, budgets, and GO/NOGO guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ico1036](https://clawhub.ai/user/ico1036) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to plan trips in Sapporo, Otaru, Yoichi, and Chitose Airport with verified restaurants, routes, weather, budgets, and GO/NOGO guidance. <br>

### Deployment Geography for Use: <br>
Global, for trips within Hokkaido, Japan. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store local trip notes and budget details. <br>
Mitigation: Keep the local vault and memory/travel-budget.json private; review or delete them before sharing or publishing the skill folder. <br>
Risk: Travel details such as restaurant hours, route timing, weather, and closures can become stale. <br>
Mitigation: Follow the skill's verification rules: refresh stale data, cross-check hours, and verify closures, routes, fares, and weather with live sources before answering. <br>


## Reference(s): <br>
- [Travel Vault README](references/vault/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/ico1036/hokkaido-travel-companion) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown travel guidance with sourced summaries, route details, budget checks, and local note updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local vault notes and memory/travel-budget.json when the user provides trip details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
