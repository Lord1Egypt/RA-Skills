## Description: <br>
Audits user-supplied websites for HTTP security headers, grades the result, and reports missing headers, weak values, and information-leak headers with recommended fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site reliability engineers, and security reviewers use this skill to run quick authorized checks of website HTTP response headers and receive actionable hardening recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound HTTP(S) requests to user-supplied URLs. <br>
Mitigation: Use it only against sites you own or are authorized to audit, and avoid localhost, internal network, metadata-service, or otherwise sensitive URLs unless those requests are intentional. <br>
Risk: The audit is limited to selected HTTP headers and obvious weak values, so it is not a complete web application security assessment. <br>
Mitigation: Treat results as triage and review recommendations before applying production configuration changes. <br>


## Reference(s): <br>
- [ClawHub release page for Http Sec Audit](https://clawhub.ai/Johnnywang2001/http-sec-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Human-readable terminal report or JSON array] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports one or more URL audit results with status, present and missing headers, warnings, information leaks, score, grade, and recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
