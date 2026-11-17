## Description:

Autonomous multi-client Linux server security management via SSH MCP, with scheduled audits, CVE scanning, hardening checks, confirmation-gated critical actions, and email reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyber-bye](https://clawhub.ai/user/cyber-bye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and security administrators use this skill to audit and manage Linux server fleets through SSH MCP, generate findings and reports, and queue higher-risk changes for explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad scheduled root-level control over server fleets.

Mitigation: Test in isolation first and replace the shared root key with per-host or per-client least-privilege credentials before production use.

Risk: Approval safeguards may be weak for critical or high-impact changes.

Mitigation: Authenticate approval replies through a trusted channel and remove or heavily restrict any APPROVE ALL workflow.

Risk: Client and server identifiers are used to write audit, action, CVE, and report files.

Mitigation: Validate client and server identifiers before file writes to prevent path or scope mistakes.

Risk: Some checks may expose sensitive account or package-inventory data.

Mitigation: Use derived-only outputs and redaction controls where possible, especially for /etc/shadow-derived checks and local CVE inventory fallback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyber-bye/skills/linux-security-guardian)
- [CISA Known Exploited Vulnerabilities catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [OSV.dev API documentation](https://google.github.io/osv.dev/)
- [NVD developer documentation](https://nvd.nist.gov/developers/start-here)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown reports, findings, action proposals, advisories, configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SSH MCP tools and local binaries listed in release metadata; email delivery depends on a separate email plugin or skill.]

## Skill Version(s):

1.6.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
