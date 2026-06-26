## Description: <br>
Evaluates and compares privacy solution vendors with a weighted scorecard across functionality, architecture, automation, compliance, cost, and vendor stability criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Privacy, security, procurement, and compliance teams use this skill to compare privacy management vendors, structure RFP evaluations, and produce scorecards, recommendations, and executive summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The registry identity says Kubernetes Network Policy Generator, while the artifact implements a privacy vendor scorecard. <br>
Mitigation: Install only if you intended to use the ToolWeb privacy-solution-scorecard, and verify the package identity before deployment. <br>
Risk: The skill sends submitted business evaluation details to the ToolWeb API. <br>
Mitigation: Review ToolWeb privacy and retention terms, and avoid submitting confidential procurement, vendor, budget, or compliance details unless your organization approves sharing them with ToolWeb. <br>
Risk: The skill requires TOOLWEB_API_KEY and curl, so credentials, rate limits, or network access can block execution. <br>
Mitigation: Use a dedicated ToolWeb API key, store it securely, and handle authentication, validation, and rate-limit errors as documented by the artifact. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/krishnakumarmahadevan-cmd/k8s-network-policy-generator) <br>
- [ToolWeb API portal](https://portal.toolweb.in) <br>
- [Privacy scorecard API endpoint](https://portal.toolweb.in/apis/compliance/privacy-scorecard) <br>
- [ToolWeb platform](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with weighted score summaries, vendor comparison highlights, recommendations, executive summary text, and curl examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; submitted organization, vendor, budget, and compliance evaluation details are sent to the ToolWeb API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
