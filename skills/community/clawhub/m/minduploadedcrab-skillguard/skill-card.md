## Description:

Security scanner for OpenClaw skills. Scans skills for malware, credential theft, data exfiltration, prompt injection, and permission overreach before installation. Run: python3 scripts/skillguard.py scan <skill-directory>

This skill is ready for commercial/non-commercial use.

## Publisher:

[minduploadedcrab](https://clawhub.ai/user/minduploadedcrab)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to scan OpenClaw skills before installation for credential access, data exfiltration, prompt injection, dependency issues, symlink attacks, and related permission risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can cross the intended scan boundary when handling symlinks or filesystem traversal cases.

Mitigation: Run scans in a low-privilege or isolated environment and inspect untrusted packages with symlinks before relying on results.

Risk: A package-provided .skillguard-ignore file can cause files to be skipped.

Mitigation: Do not trust package-provided ignore exclusions; review ignored paths manually before accepting a PASS verdict.

Risk: Automated scanner output is not a definitive security gate.

Mitigation: Manually review SKILL.md and high-risk behavior even when the tool reports PASS.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minduploadedcrab/skills/minduploadedcrab-skillguard)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Terminal text, audit tables, quiet verdict strings, or JSON scan reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan reports include file counts, risk score, PASS/WARN/FAIL verdict, findings, severity, category, location, and evidence when available.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
