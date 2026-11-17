## Description:

Verify signed audit evidence and inspect tenant-scoped event references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[schchit](https://clawhub.ai/user/schchit)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to run or integrate a local authenticated audit API that verifies signed audit evidence, stores tenant-scoped event records, and supports permissioned reads and exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored audit events and exported reports may contain sensitive operational evidence.

Mitigation: Treat the SQLite database, backups, and exports as sensitive data; use a private database path and restrict file access to the service account.

Risk: Exposing the API beyond loopback without perimeter controls can increase unauthorized access and denial-of-service risk.

Mitigation: Run on 127.0.0.1 by default; for remote use, terminate TLS and enforce request-rate and read-time limits at a trusted reverse proxy.

Risk: Weak bearer tokens, incorrect trusted keys, or missing tenant quotas can undermine authentication, signature verification, or storage isolation.

Mitigation: Configure strong bearer tokens, out-of-band trusted public keys, least-privilege permissions, and operator-controlled tenant quotas before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/schchit/skills/jep-guard-audit)
- [Security profile](SECURITY.md)
- [README](README.md)
- [Release changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, Python code, configuration examples, and JSON API outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local authenticated audit service; outputs and exports may contain sensitive operational evidence.]

## Skill Version(s):

2.0.1 (source: server release metadata, SKILL.md frontmatter, manifest.json, BUILD-INFO.json, and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
