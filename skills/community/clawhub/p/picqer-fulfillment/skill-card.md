## Description: <br>
Provides JSON API commands to fetch Picqer dashboard KPIs, picklists, stock movements, and revenue data for order fulfillment monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnmcgucki](https://clawhub.ai/user/johnmcgucki) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Fulfillment operators and business users can use this skill to retrieve Picqer dashboard data for order monitoring, picker performance, stock movement review, and sell-stock client revenue analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local Picqer API key and returns operational dashboard data that may be sensitive. <br>
Mitigation: Install only in a trusted workspace, use a least-privilege Picqer API key, and treat returned dashboard data as sensitive business information. <br>
Risk: The artifact states Tailscale-only access, but the provided code does not enforce that network boundary. <br>
Mitigation: Verify and enforce network access controls in the deployment environment before exposing the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnmcgucki/picqer-fulfillment) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Guidance] <br>
**Output Format:** [JSON objects containing dashboard KPIs, picklists, stock movements, revenue data, filters used, or structured error messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands include dashboard.fetch, picklists.fetch, stock.fetch, and revenue.fetch with optional date, picker, and client filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
