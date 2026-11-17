## Description:

Scans a macOS computer for signs of tampering, malware, keyloggers, and suspicious activity, especially after a device has been repaired or handled by a third party.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentyao](https://clawhub.ai/user/vincentyao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support-oriented agents use this skill to run a read-only macOS security inventory, summarize suspicious findings, and produce a local report after repair, third-party handling, or suspected tampering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local report can expose sensitive system, application, permission, and network information.

Mitigation: Keep the report local and avoid sharing it publicly; share it only with a trusted security professional or support contact when needed.

Risk: Optional sudo mode gives the scanner deeper read access to macOS security state.

Mitigation: Use sudo mode only when the user explicitly wants deeper results and understands that it expands what the scanner can read.

Risk: Security findings may be incomplete or require human interpretation.

Mitigation: Treat the scan as a first check, verify unfamiliar findings before acting, and use dedicated antivirus software or professional support for high-risk cases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vincentyao/skills/macos-security-scan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report plus plain-English chat summary and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated report is saved locally as ~/Desktop/security_report.md and may contain sensitive system, app, permission, and network details.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
