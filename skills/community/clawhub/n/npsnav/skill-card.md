## Description: <br>
Query Indian NPS (National Pension System) fund NAV data, scheme info, returns, and history via the free npsnav.in REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kanaksinghal](https://clawhub.ai/user/kanaksinghal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and finance operations teams use this skill to look up Indian National Pension System scheme codes, latest NAVs, fund details, returns, and historical NAV data through public API queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested NPS scheme codes are sent to the public npsnav.in API. <br>
Mitigation: Avoid querying sensitive or unintended scheme selections, and review commands before execution. <br>
Risk: Returned NAV and performance data may be incomplete, stale, or unsuitable as the sole basis for financial decisions. <br>
Mitigation: Verify NAV, return, and scheme information against authoritative financial sources before relying on it. <br>


## Reference(s): <br>
- [Npsnav ClawHub Release](https://clawhub.ai/kanaksinghal/npsnav) <br>
- [npsnav.in](https://npsnav.in) <br>
- [NPS Funds List](https://npsnav.in/nps-funds-list) <br>
- [npsnav.in API Base](https://npsnav.in/api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Text, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON or plain-text API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; no authentication or API keys are required.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
