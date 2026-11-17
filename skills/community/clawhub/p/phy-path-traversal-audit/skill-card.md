## Description:

Path traversal and Local File Inclusion scanner for Python, Java, PHP, Node.js, Go, and Ruby code that reports CWE-22/CWE-98 findings and safer path-handling guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to scan source repositories for path traversal and Local File Inclusion patterns and receive findings with remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shipped artifact may not provide a working scanner, which can create false security confidence.

Mitigation: Review before installing and verify scanner execution on known vulnerable and clean test fixtures before relying on reports.

Risk: Using this skill as a CI security gate before the scanner is packaged and tested may miss or misreport vulnerabilities.

Mitigation: Do not enforce it as a CI security gate until executable packaging, import-time behavior, and expected detections are tested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-path-traversal-audit)
- [Canlah AI homepage](https://canlah.ai)
- [OWASP Top 10 A01:2021 Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Code, Shell commands, Guidance]

**Output Format:** [Markdown reports with optional JSON findings and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports severity, CWE classification, HTTP taint context, and remediation guidance for detected path traversal and LFI patterns.]

## Skill Version(s):

1.0.3 (source: server release metadata, target metadata, and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
