## Description: <br>
Evaluate and compare privacy solution vendors with a weighted scorecard across 12 criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and security, privacy, procurement, and compliance teams use this skill to compare privacy management vendors, evaluate consent and data protection platforms, and build privacy tool business cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends organization, evaluator, budget, regulation, vendor, scoring, and notes data to a third-party ToolWeb API. <br>
Mitigation: Confirm exactly what will be transmitted before calling the API, redact sensitive fields, and review ToolWeb retention and access practices before use. <br>
Risk: Successful API calls are tracked for billing. <br>
Mitigation: Confirm the configured API key, plan limits, and expected cost exposure before running comparisons. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/krishnakumarmahadevan-cmd/privacy-solution-scorecard) <br>
- [ToolWeb portal](https://portal.toolweb.in) <br>
- [Privacy scorecard API endpoint](https://portal.toolweb.in/apis/compliance/privacy-scorecard) <br>
- [ToolWeb platform](https://toolweb.in) <br>
- [ToolWeb OpenClaw skills](https://toolweb.in/openclaw/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with API-backed scorecard results; API response fields contain HTML report sections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; expected outputs include vendor ranking, comparison highlights, recommendations, and an executive summary.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
