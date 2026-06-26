## Description: <br>
Analyze HTTP security headers for user-specified URLs, grade website posture A-F, and provide OWASP-aligned recommendations and server-specific fix snippets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and site operators use this skill to inspect HTTP response headers for websites they own or are authorized to test, identify missing or weak security controls, and generate prioritized remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner contacts each URL supplied by the user, including every URL in batch mode. <br>
Mitigation: Use it only on domains or systems the user owns or is authorized to test, and review batch URL lists before execution. <br>


## Reference(s): <br>
- [HTTP Security Headers ClawHub Page](https://clawhub.ai/charlie-morrison/http-security-headers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Text, JSON, or Markdown reports with grades, findings, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Batch mode can report on multiple user-supplied URLs and CI mode can return grade-based exit codes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
