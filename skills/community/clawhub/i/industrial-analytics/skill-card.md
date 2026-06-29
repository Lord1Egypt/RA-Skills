## Description: <br>
Provides read-only OT analytics through the ot-aiops MCP server for OEE computation, downtime analysis, multi-dimensional OEE aggregation, active asset inventory, and bounded change-of-value monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and industrial engineers use this skill to ask agents for read-only OEE, downtime, asset inventory, and change monitoring analysis across configured OT endpoints. It is intended for analytics and reporting workflows, not device writes or broad IT infrastructure troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Active asset fingerprinting and bounded polling can add connection load to configured industrial devices. <br>
Mitigation: Confirm endpoints are intentionally configured and that fingerprinting or polling is allowed by site procedures before use. <br>
Risk: Analytics results may be misleading if production, state-series, or endpoint inputs are incomplete or incorrect. <br>
Mitigation: Review input sources and outputs before using generated OEE, downtime, inventory, or change-monitoring results for operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/industrial-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON structures and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only analytics guidance; active inventory and polling must be intentionally configured.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
