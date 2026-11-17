## Description:

Scan binaries and scripts for malicious patterns before trusting them. Use when installing skills, evaluating unknown binaries, or auditing tool dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dev-null321](https://clawhub.ai/user/dev-null321)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use OpenScan to perform lightweight static checks on macOS and Linux binaries, scripts, and skill folders before trusting or installing them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server security evidence reports a suspicious verdict and a command-injection issue when scanning specially named files on macOS.

Mitigation: Do not run the scanner with sudo or against untrusted macOS files until the code-signature check uses an argument-array API such as execFileSync.

Risk: The scanner is lightweight static analysis and can miss runtime-only behavior, sophisticated obfuscation, custom packers, or malware not covered by its patterns.

Mitigation: Use results as review signals, not final security decisions, and pair them with deeper antivirus, EDR, sandboxing, or manual review for high-risk artifacts.

Risk: Legitimate security tools, debuggers, and system utilities may trigger false positives.

Mitigation: Manually review suspicious findings before blocking or trusting a dependency.

## Reference(s):

- [OpenScan ClawHub listing](https://clawhub.ai/dev-null321/skills/openscan)
- [Harkonnen antimalware engine](https://github.com/dev-null321/Harkonnen)
- [OpenScan repository](https://github.com/dev-null321/openScan)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable terminal report or JSON scan results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes file hashes, threat scores from 0-100, findings, and exit codes 0, 1, or 2 for automation.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
