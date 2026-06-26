## Description: <br>
Perform ISO compliance gap analysis for ISO 27001, ISO 27701, and ISO 42001 standards for certification readiness, information security gaps, privacy management gaps, AI management system compliance, and multi-standard ISO audit preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External security, privacy, compliance, and audit-preparation teams use this skill to collect ISO readiness inputs, call ToolWeb's ISO gap analysis API, and present per-standard scores, gaps, strengths, and prioritized remediation recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security, privacy, and audit-readiness answers are sent to ToolWeb for API-based analysis. <br>
Mitigation: Obtain organizational approval before use and avoid submitting secrets, regulated personal data, or confidential audit evidence unless disclosure to ToolWeb is approved. <br>
Risk: The skill requires a ToolWeb API key and successful calls may affect quota or billing. <br>
Mitigation: Use a dedicated, revocable API key, store it in TOOLWEB_API_KEY, and monitor account usage and rate limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/iso-compliance-gap-analysis) <br>
- [ToolWeb platform](https://toolweb.in) <br>
- [ToolWeb API portal](https://portal.toolweb.in) <br>
- [ISO gap analysis API endpoint](https://portal.toolweb.in/apis/compliance/iso-gap-analysis) <br>
- [ToolWeb OpenClaw skills](https://toolweb.in/openclaw/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with compliance scores, standard-by-standard gaps and strengths, and prioritized recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; sends assessment responses to ToolWeb for API-based analysis.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
