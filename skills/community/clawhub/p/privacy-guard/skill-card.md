## Description:

Protects sensitive files (contracts, transaction data, personal/customer privacy) by performing deep content inspection for text and binary formats (PDF, DOCX, XLSX) before any read, search, or send operation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yacki](https://clawhub.ai/user/yacki)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to scan local files for sensitive content before reading, searching, or sending those files. It is aimed at reducing accidental disclosure of contracts, transaction records, personal privacy data, customer data, and company-confidential material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keyword-based local scanning can miss sensitive information and may return PASS for files that still contain private data.

Mitigation: Treat PASS as advisory and avoid relying on the scanner as the sole privacy barrier before external transmission.

Risk: The skill strongly controls file workflows and can block or interrupt normal agent operations when sensitive keywords are detected.

Mitigation: Review BLOCK results with the user and proceed only when the intended operation is appropriate and separately authorized.

Risk: The scanner depends on third-party Python packages for PDF, DOCX, and XLSX parsing.

Mitigation: Install dependencies in an isolated environment and review or pin dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yacki/skills/privacy-guard)
- [Publisher profile](https://clawhub.ai/user/yacki)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text scan results and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scanner accepts a local file path and returns PASS, BLOCK, or ERROR status text.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
