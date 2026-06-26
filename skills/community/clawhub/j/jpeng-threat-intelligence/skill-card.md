## Description: <br>
Get threat intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security practitioners and developers use this skill to run threat-intelligence lookups, automate intel tasks, and support security operations workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external threat-intelligence provider and API-key handling are not clearly explained. <br>
Mitigation: Install only when the intended provider and script are known, and use a limited or disposable INTEL_API_KEY where possible. <br>
Risk: Threat-intelligence queries may send confidential incident data to an external service. <br>
Mitigation: Avoid submitting confidential data unless the provider is trusted and its retention policies are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-threat-intelligence) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires INTEL_API_KEY for the external threat-intelligence service.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
