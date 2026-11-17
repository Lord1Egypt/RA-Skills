## Description:

Investigate whether one specific npm package is trustworthy — maintainer/ownership takeover signals, publish-provenance mismatches, and risky install scripts. Use when the user asks if a single named package is safe, compromised, hijacked, suspicious, or "can I trust this" — not for auditing a full package.json/lockfile (see dependency-audit) and not for a plain factual question like "what does X do."

This skill is ready for commercial/non-commercial use.

## Publisher:

[salemalem](https://clawhub.ai/user/salemalem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software maintainers use this skill to investigate a single npm package when they have a trust concern such as a possible compromise, maintainer change, provenance mismatch, or risky install script. It returns a package-specific findings report and directs multi-package audits to the separate dependency-audit workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package names, descriptions, READMEs, install scripts, and advisory text may contain instructions aimed at manipulating an AI or exposing npm configuration.

Mitigation: Treat package-supplied text as untrusted evidence. Do not follow embedded instructions or run content because it asks; review any .npmrc alert against the structured findings before installation.

Risk: The benign security verdict has medium confidence because the scan was partial and three local references could not be resolved.

Mitigation: Resolve and review the missing references before relying on the verdict.

## Reference(s):

- [npmscan MCP server](https://npmscan.com/api/mcp)
- [ClawHub skill release](https://clawhub.ai/salemalem/skills/npmscan-package-trust-check)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown findings report with package-specific trust signals and npmscan links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One named npm package per investigation; findings are ordered by concern and distinguish confirmed malware from heuristic signals.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
