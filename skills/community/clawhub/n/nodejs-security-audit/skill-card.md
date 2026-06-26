## Description: <br>
Audit Node.js HTTP servers and web apps for security vulnerabilities. Checks OWASP Top 10, CORS, auth bypass, XSS, path traversal, hardcoded secrets, missing headers, rate limiting, and input validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npfaerber](https://clawhub.ai/user/npfaerber) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to review Node.js HTTP servers and web applications before deployment or after changes, with a checklist for common web security risks and a structured audit report format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit results may contain sensitive project details, vulnerability descriptions, file paths, or discovered secrets. <br>
Mitigation: Review and redact generated findings before sharing them outside the authorized review team. <br>
Risk: The checklist can surface issues in codebases the user is not authorized to inspect. <br>
Mitigation: Use the skill only on systems and repositories where the reviewer has explicit authorization. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown security audit report with checklist findings and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive file paths, vulnerability details, or discovered secrets; review and redact before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
