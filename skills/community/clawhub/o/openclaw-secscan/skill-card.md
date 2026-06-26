## Description: <br>
Security analysis and vulnerability detection. Scans code for security issues, checks dependencies, and provides remediation advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run local security checks for Python source files, dependency manifests, and possible secrets before release or CI handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads files under the directories selected by the user. <br>
Mitigation: Run it only against directories you intend to inspect and avoid broad scans over unrelated sensitive workspaces. <br>
Risk: Secret-detection output can expose sensitive findings in terminal or CI logs. <br>
Mitigation: Restrict log access, avoid publishing scan output, and rotate any credentials reported by the scan. <br>
Risk: Dependency checks are informational and do not replace a dedicated vulnerability audit. <br>
Mitigation: Use a dependency auditing tool such as pip-audit or safety for authoritative vulnerability checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michealxie001/openclaw-secscan) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text console output with findings, CWE identifiers when available, and remediation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file paths, line numbers, masked secret matches, and suggested follow-up tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
