## Description:

Applies NIST/CWE security hardening to Python and Rust code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to audit a repository for security weaknesses and receive citation-backed findings and concrete remediation proposals. It supports Python and Rust checks, cross-cutting supply-chain and CI checks, and NIST SSDF mapping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit summaries and dependency names may reveal information about a repository when reports are shared.

Mitigation: Review report contents before sharing and limit access to audit summaries and dependency details.

Risk: Some security guidance, including Rust guidance, may be incomplete or misleading; the scanner could not inspect some referenced paths.

Mitigation: Review the Rust guidance and inspect the referenced paths, then validate recommendations against the repository and cited security references before applying them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-pensive-harden)
- [Pensive project homepage (listed in Clawdis metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)
- [Python hardening checks](modules/python-checks.md)
- [Rust hardening checks](modules/rust-checks.md)
- [Cross-cutting hardening checks](modules/cross-cutting.md)
- [NIST and CWE citation backbone](modules/nist-controls.md)
- [Remediation proposal format](modules/proposal-shape.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Configuration instructions, Shell commands]

**Output Format:** [Markdown audit reports and remediation proposals with code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include security references; proposed changes are presented for user review and approval.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
