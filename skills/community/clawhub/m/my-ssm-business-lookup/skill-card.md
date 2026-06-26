## Description: <br>
Looks up Malaysian company registration data from SSM and returns structured company details including directors, status, filings, and business type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wms2537](https://clawhub.ai/user/wms2537) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to check Malaysian business registration records by company name or registration number before continuing workflows that need company identity or status details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill charges 0.05 USDT per call through SkillPay. <br>
Mitigation: Require user confirmation before each paid lookup and show the per-call price before execution. <br>
Risk: Company names or registration numbers are sent to an external lookup service. <br>
Mitigation: Avoid submitting sensitive or confidential lookup queries unless the user accepts the external data-sharing behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wms2537/my-ssm-business-lookup) <br>
- [Publisher profile](https://clawhub.ai/user/wms2537) <br>
- [Project homepage](https://github.com/swmeng/myskills) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON response with structured company data or lookup and billing errors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SKILLPAY_API_KEY and charges 0.05 USDT per successful call.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
