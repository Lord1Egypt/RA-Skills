## Description:

Security analysis and vulnerability detection. Scans code for security issues, checks dependencies, and provides remediation advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan code and dependency manifests for security issues, detect likely secret exposure, and receive remediation guidance before release or CI deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scan output can expose sensitive values or file contents from target directories.

Mitigation: Run the skill only on intended directories, review output before sharing it, and avoid publishing logs to shared CI until output redaction is verified.

Risk: Optional C/C++ support imports code from outside the skill package when that path exists.

Mitigation: Package the optional C support inside the released skill or integrity-check the external support library before trusting C/C++ findings.

Risk: Dependency checks are informational and may not provide a complete vulnerability audit.

Mitigation: Confirm dependency risk with a maintained vulnerability scanner before treating results as release-blocking.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style terminal output with findings, severity labels, CWE identifiers, and remediation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scanned file paths, line numbers, issue summaries, dependency-check instructions, and masked secret snippets.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
