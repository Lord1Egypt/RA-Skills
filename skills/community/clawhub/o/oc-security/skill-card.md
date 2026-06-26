## Description: <br>
Security analysis and vulnerability detection. Scans code for security issues, checks dependencies, and provides remediation advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to run local checks for code vulnerabilities, dependency issues, exposed secrets, and C/C++ security patterns before review or release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency results are informational and may not constitute a complete vulnerability audit. <br>
Mitigation: Use dedicated dependency-audit tools and treat this skill's dependency output as a starting point for review. <br>
Risk: Secret detection output may expose sensitive values in logs or shared terminals. <br>
Mitigation: Run secret scans only in controlled terminals or CI jobs with secured logs, and rotate any credentials that are detected. <br>
Risk: C/C++ scanning depends on an adjacent support library and may be unavailable or incomplete. <br>
Mitigation: Confirm the C/C++ support dependency is present and trusted before relying on C/C++ findings, and treat missing-support warnings as coverage gaps. <br>
Risk: The security evidence notes that the skill may overstate some scanning capabilities. <br>
Mitigation: Validate important findings with independent scanners and human review before using the results for release decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michealxie001/oc-security) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text with finding summaries and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports findings by file, line, severity, CWE, and suggested fix when available.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
