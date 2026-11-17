## Description:

Scan AI agent skills for security vulnerabilities including code injection, prompt injection, credential exfiltration, supply chain attacks, and other threat patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xrapi](https://clawhub.ai/user/0xrapi)

### License/Terms of Use:


## Use Case:

Developers, security reviewers, and agents use this skill to scan skill directories, packages, and code contributions before installation, review, publishing, or CI integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on an unpinned third-party package.

Mitigation: Install only from a trusted package source and prefer a pinned or reviewed package version where possible.

Risk: CVE checks may make network requests to external vulnerability services.

Mitigation: Use CVE checking only when external network access is acceptable for the files and environment being scanned.

Risk: Broad scan targets can include files outside the intended review scope.

Mitigation: Run scans on the specific directories or packages intended for inspection.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xrapi/skills/isnad-scan)
- [Publisher Profile](https://clawhub.ai/user/0xrapi)
- [ISNAD Protocol](https://isnad.md)
- [ISNAD Project Repository](https://github.com/counterspec/isnad)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, code snippets, and optional JSON scanner output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide use of verbose, CVE, and JSON output modes from the installed scanner.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
