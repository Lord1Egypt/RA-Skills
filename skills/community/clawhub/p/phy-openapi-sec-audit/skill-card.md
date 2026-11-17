## Description:

OpenAPI/Swagger security auditor that scans OpenAPI 3.x and Swagger 2.0 YAML or JSON specs for authentication, transport, OAuth, sensitive response data, input validation, admin endpoint, upload, scope, and auth response misconfigurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and API platform teams use this skill to audit OpenAPI and Swagger specifications before release or in CI. It helps identify common API security misconfigurations and produces actionable findings with severity, CWE mapping, and suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote URL scanning can fetch arbitrary HTTP/HTTPS locations from the agent's environment, including from CI runners, cloud VMs, corporate networks, or agent environments with internal access.

Mitigation: Prefer local OpenAPI spec files; when remote URL scanning is necessary, avoid untrusted URLs and run with network egress controls or inside a sandbox.

Risk: YAML support depends on installing PyYAML, which can affect reproducibility if dependency versions are left floating.

Mitigation: Install PyYAML in an isolated environment and pin dependencies where reproducible scans matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-openapi-sec-audit)
- [Publisher profile](https://clawhub.ai/user/phy041)
- [Homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and CLI-style audit findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity labels, CWE identifiers, affected OpenAPI paths, and remediation guidance.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
