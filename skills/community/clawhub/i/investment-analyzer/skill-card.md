## Description: <br>
Analyzes rental properties, ETFs, real estate-versus-ETF allocations, Centris listings, and DCA plans with data-backed investment verdicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clairproqc-star](https://clawhub.ai/user/clairproqc-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to help investors structure property, ETF, allocation, and DCA analyses using bundled criteria, helper scripts, and consistent BUY / INVESTIGATE / PASS-style conclusions. It is most applicable to Canadian and Quebec-focused real estate and ETF scenarios. <br>

### Deployment Geography for Use: <br>
Canada, with Quebec-specific assumptions <br>

## Known Risks and Mitigations: <br>
Risk: The artifact bundles personal financial profile and portfolio details. <br>
Mitigation: Remove or replace the bundled profile and portfolio files before use, and do not publish or share generated analyses containing private financial details. <br>
Risk: Investment conclusions can be wrong if rates, taxes, rents, market prices, holdings, or assumptions are stale or incomplete. <br>
Mitigation: Verify all inputs against current sources and treat outputs as decision support, not professional financial, tax, legal, or mortgage advice. <br>
Risk: The skill declares a Gemini API key requirement and scripts may contact external market or listing services. <br>
Mitigation: Confirm whether the API key is required in the target environment and only run workflows with data you are comfortable exposing to the agent and external services. <br>


## Reference(s): <br>
- [Investment Analyzer ClawHub listing](https://clawhub.ai/clairproqc-star/investment-analyzer) <br>
- [Decision criteria](references/criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis with metric tables and final verdicts; helper scripts return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses BUY, INVESTIGATE, PASS, ADD, SKIP, ETF WINS, REAL ESTATE WINS, and TOO CLOSE TO CALL verdict labels depending on workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
