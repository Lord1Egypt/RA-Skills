## Description: <br>
Use when auditing Go code involving logging, error handling, HTTP response data, Kubernetes Secret management, or credential storage for information disclosure risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhy0](https://clawhub.ai/user/yhy0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to audit Go code for possible credential leaks, information disclosure in logs and API responses, Kubernetes Secret handling mistakes, and related CWE-200/532/522/312/552 patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks the skill as suspicious because it includes high-impact auth and RCE guidance outside its stated information-disclosure scope. <br>
Mitigation: Use the skill only as a broader Go security-audit reference on codebases you are authorized to review, and route discovered secrets or exploit-relevant findings through approved private disclosure channels. <br>


## Reference(s): <br>
- [Go Information Disclosure Real-World Cases](references/cases.md) <br>
- [ClawHub skill page](https://clawhub.ai/yhy0/go-vuln-info-disclosure) <br>
- [Publisher profile](https://clawhub.ai/user/yhy0) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with grep command examples and audit checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no tools or APIs are invoked by the skill itself.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
