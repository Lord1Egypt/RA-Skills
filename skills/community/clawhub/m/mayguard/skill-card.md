## Description:

A security auditor for agent skills. Scans skill directories for malicious patterns (credential theft, suspicious network calls, destructive commands) and provides a safety score. Use before installing unknown skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[balkanblbn](https://clawhub.ai/user/balkanblbn)

### License/Terms of Use:


## Use Case:

Developers and agent operators use MayGuard to run a lightweight static audit of unknown skill directories before installation. It reports suspicious patterns such as credential access, outbound networking, destructive commands, and obfuscation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit can read outside the chosen audit folder through symlinks.

Mitigation: Audit untrusted skills in a sandbox and prefer a fixed version that rejects symlinks.

Risk: The audit can miss hidden files, archives, and skipped file types.

Mitigation: Do not rely on a SAFE result unless hidden files, archives, and skipped files have also been reviewed.

Risk: The tool is a lightweight helper rather than a definitive safety gate.

Mitigation: Use its findings as one review input and perform manual review before installing or deploying untrusted skills.

## Reference(s):

- [Threat Patterns](references/threat_patterns.json)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Text audit report, with optional JSON output when --json is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes status, risk score, and pattern findings; hidden files, archives, and symlinks require separate handling before relying on a SAFE result.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
