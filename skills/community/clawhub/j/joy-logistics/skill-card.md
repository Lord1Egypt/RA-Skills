## Description: <br>
Joy Logistics helps OpenClaw agents query JD international logistics tracking, supply-chain operations metrics, and cross-border parcel experience metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joy-logistics](https://clawhub.ai/user/joy-logistics) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Logistics operations users and agents use this skill to retrieve shipment tracking details and operational KPI data for JD international logistics workflows, then present query results and analysis in Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles API tokens and shipment or business identifiers. <br>
Mitigation: Use it only with trusted publishers, authorized logistics queries, and least-privilege token storage; rotate any token already used with this version if exposure is possible. <br>
Risk: The security evidence reports unsafe TLS settings in the query scripts. <br>
Mitigation: Fix the scripts to validate TLS certificates before relying on the skill for sensitive logistics data. <br>


## Reference(s): <br>
- [Joy Logistics ClawHub page](https://clawhub.ai/joy-logistics/joy-logistics) <br>
- [joy-logistics publisher profile](https://clawhub.ai/user/joy-logistics) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, markdown, JSON, guidance] <br>
**Output Format:** [Markdown responses with shell command invocations and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries require an environment token and user-provided shipment, date, metric, warehouse, customer, or dimension parameters.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
