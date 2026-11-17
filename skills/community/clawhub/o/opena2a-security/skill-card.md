## Description:

OpenA2A Security helps agents audit OpenClaw configuration, scan installed skills for security issues, detect CVE-2026-25253 exposure, check credential handling, and provide actionable remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdelsfane](https://clawhub.ai/user/abdelsfane)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to audit OpenClaw installations, check installed skills and configuration for security issues, detect CVE-2026-25253 exposure, and receive remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run an unpinned npm scanner against sensitive OpenClaw files.

Mitigation: Run only a pinned, trusted HackMyAgent version or a locked local install; prefer mounting ~/.openclaw read-only during scans.

Risk: The security evidence notes a no-network-use claim while the scanner is invoked through npx.

Mitigation: Block outbound network during scans when possible and review the scanner package before execution.

Risk: Generated reports may contain sensitive configuration findings or file paths.

Mitigation: Treat reports as sensitive local artifacts and avoid sharing them without review and redaction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abdelsfane/skills/opena2a-security)
- [HackMyAgent npm package](https://www.npmjs.com/package/hackmyagent)
- [HackMyAgent repository](https://github.com/opena2a-org/hackmyagent)
- [OpenClaw trust threat model](https://github.com/openclaw/trust/pull/7)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, markdown, code]

**Output Format:** [Markdown guidance with inline shell commands and scanner report references; reports may be generated as text, JSON, SARIF, HTML, or ASP.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local OpenClaw security checks through HackMyAgent and may produce security findings, remediation steps, and report files.]

## Skill Version(s):

1.0.0 (source: frontmatter, evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
