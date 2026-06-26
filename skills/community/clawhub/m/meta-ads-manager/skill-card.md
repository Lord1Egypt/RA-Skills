## Description: <br>
Manage and analyze Meta (Facebook/Instagram) ad campaigns, including performance reporting, audience and creative analysis, budget optimization, and confirmed campaign, ad set, or ad changes through Meta Marketing API access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiddun](https://clawhub.ai/user/aiddun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External advertisers, marketers, and agency operators use this skill to inspect connected Meta ad accounts, summarize campaign performance, diagnose audiences and creatives, optimize budgets, and perform explicitly confirmed campaign management changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated Meta ad account access can expose campaign, spend, and performance data from connected accounts. <br>
Mitigation: Install only after trusting the Metacog OAuth connection and connect only the Meta ad accounts the agent should inspect or manage. <br>
Risk: Confirmed write actions can change campaigns, ad sets, ads, or budgets. <br>
Mitigation: Approve write actions only when the exact account, target object, current value, new value, and rollback path are clear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiddun/meta-ads-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, API Calls] <br>
**Output Format:** [Markdown summaries and tables, with API-backed readouts and explicitly confirmed write actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses concise aggregated outputs, capped ranked lists, formatted metrics, and persisted context for follow-up ad account analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
