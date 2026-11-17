## Description:

MUKI Asset Fingerprinting helps agents support authorized red-team reconnaissance with active and passive service fingerprinting, sensitive path checks, and sensitive information extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[admin4giter](https://clawhub.ai/user/admin4giter)

### License/Terms of Use:

MIT

## Use Case:

Security engineers and authorized assessors use this skill to plan and run asset discovery, service fingerprinting, vulnerability-oriented reconnaissance, and review of sensitive path or data findings within a written testing scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthorized or out-of-scope scanning can create legal and operational risk.

Mitigation: Use only for authorized assessments with written scope covering targets, timing, and permitted techniques.

Risk: Active probes can touch sensitive services or generate traffic beyond what a broad assessment permits.

Mitigation: Review active rules before use, disable active probing or directory checks when not approved, and lower thread counts for controlled scans.

Risk: Scan reports can contain credentials, personal data, and internal service details.

Mitigation: Treat reports as restricted evidence and redact, encrypt, and limit access before storing or sharing results.

Risk: Fingerprint and sensitive-data matches can include false positives.

Mitigation: Manually validate findings before escalation, remediation requests, or use with downstream exploitation tools.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/admin4giter/skills/muki-fingerprint)
- [MUKI Quick Reference](references/quick-reference.md)
- [Extraction Rules](references/Rules.yml)
- [Active Fingerprint Rules](references/active_finger.json)
- [Compact Active Fingerprint Rules](references/active_finger精简.json)
- [Passive Fingerprint Database](references/finger.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or Excel report descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide commands that produce JSON or .xlsx scan reports when executed in an authorized environment.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
