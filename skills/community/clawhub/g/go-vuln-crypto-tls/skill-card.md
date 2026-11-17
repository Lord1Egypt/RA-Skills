## Description:

Use when auditing Go code involving TLS configuration, certificate validation, JWT token parsing, SAML assertion verification, webhook signature checking, or cryptographic operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhy0](https://clawhub.ai/user/yhy0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to audit Go code paths that implement TLS, certificate validation, JWT parsing, SAML validation, webhook HMAC checks, and related cryptographic verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The real-world case notes contain placeholder CVE and CVSS values that may be mistaken for authoritative vulnerability records.

Mitigation: Verify each case identifier, severity, and affected-version claim against authoritative advisories before citing it in an audit report.

Risk: The skill body is written primarily in Chinese, which may reduce reviewer comprehension in teams that cannot review Chinese-language security guidance.

Mitigation: Use the skill only where Chinese-language audit guidance is acceptable, or translate and review the guidance before adoption.

Risk: Grep-based detection paths can surface false positives in tests, development-only configuration, or non-authentication uses of cryptographic APIs.

Mitigation: Apply the artifact's false-positive exclusion guidance and require human review before reporting candidate findings.

## Reference(s):

- [Go Crypto/TLS Real-World Cases](references/cases.md)
- [ClawHub skill page](https://clawhub.ai/yhy0/skills/go-vuln-crypto-tls)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with grep commands, Go code patterns, and audit checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only audit guidance; no hidden execution, credential use, or persistence found in security evidence.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
