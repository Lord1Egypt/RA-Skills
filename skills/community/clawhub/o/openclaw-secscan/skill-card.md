## Description:

Security analysis and vulnerability detection for scanning code, checking dependencies, and providing remediation advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan Python code for common security issues, check dependency files, and detect likely secrets before code is shared or integrated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secret-scanning output can disclose real credentials into terminal or CI logs.

Mitigation: Use the skill only on directories intended for scanning, avoid running secrets --dir . on workspaces with real credentials, do not publish or retain scanner output until redaction is fixed, and rotate any credentials printed by this version.

## Reference(s):

- [OpenClaw Security Scanner on ClawHub](https://clawhub.ai/michealxie001/skills/openclaw-secscan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and scanner result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file paths, line numbers, severity labels, CWE identifiers, dependency-check suggestions, and secret-detection findings.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
