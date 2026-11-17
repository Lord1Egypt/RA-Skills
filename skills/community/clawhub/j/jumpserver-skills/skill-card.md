## Description:

JumpServer helps agents initialize JumpServer V4 configuration and perform read-only asset, permission, audit, and access queries through bundled CLI scripts without performing business mutations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liqiang-fit2cloud](https://clawhub.ai/user/liqiang-fit2cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to initialize JumpServer V4 access, select an organization, troubleshoot assets and permissions, investigate audits, and analyze access while keeping business-object changes out of scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JumpServer credentials and generated .env.local files can expose privileged access if mishandled.

Mitigation: Use least-privilege JumpServer credentials, protect .env.local, and avoid sharing command payloads or logs that contain secrets.

Risk: Untrusted config-write payload values can alter the JumpServer target, authentication mode, or organization context.

Mitigation: Review config-write and select-org previews before confirming, and rerun the full preflight flow after changing targets, accounts, or orgs.

Risk: Custom JMS_SDK_MODULE or JMS_SDK_GET_CLIENT settings can redirect runtime behavior to untrusted code.

Mitigation: Leave custom SDK module settings unset unless the module and factory function are fully trusted and reviewed.

Risk: The documented runtime disables TLS certificate verification and suppresses HTTPS certificate warnings.

Mitigation: Prefer a release that verifies TLS certificates; until then, restrict use to trusted JumpServer endpoints and reviewed environments.

Risk: Dependency versions are not fully pinned, which can change runtime behavior across installations.

Mitigation: Install in a controlled environment with reviewed, pinned dependency versions before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liqiang-fit2cloud/skills/jumpserver-skills)
- [Runtime Behavior](artifact/references/runtime-behavior.md)
- [Query Boundaries](artifact/references/query-boundaries.md)
- [Preflight and Diagnostics](artifact/references/preflight-and-diagnostics.md)
- [Object Queries](artifact/references/object-queries.md)
- [Permission Queries](artifact/references/permission-queries.md)
- [Audit Queries](artifact/references/audit-queries.md)
- [Object Map](artifact/references/object-mapping.md)
- [Troubleshooting Guide](artifact/references/troubleshooting-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-style query result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or update .env.local and persist JMS_ORG_ID only through documented confirmation flows; business object and permission mutations are out of scope.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
