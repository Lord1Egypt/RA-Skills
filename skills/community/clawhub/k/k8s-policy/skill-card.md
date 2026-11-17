## Description:

Manage Kubernetes policies with Kyverno and Gatekeeper to enforce security rules, validate resources, and audit compliance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Kubernetes operators use this skill to inspect Kyverno and Gatekeeper policies, review compliance violations, and create policy manifests for Kubernetes clusters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Policy enforcement may affect cluster resources when the target scope and rollout safeguards are unclear.

Mitigation: Select the intended cluster and namespaces, start in Kyverno Audit or Gatekeeper dryrun, review violations, approve enforcement separately, and prepare a rollback procedure.

Risk: Installing policy controllers from unpinned manifests may introduce unexpected changes.

Mitigation: Pin and inspect controller installation manifests before applying them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/rohitg00/skills/k8s-policy)
- [Kyverno MCP server](https://github.com/nirmata/kyverno-mcp)
- [Kyverno installation manifest](https://github.com/kyverno/kyverno/releases/latest/download/install.yaml)
- [Gatekeeper installation manifest](https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration, Shell commands]

**Output Format:** [Markdown with tool-call examples, shell commands, and YAML policy manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Kubernetes policy examples and operational guidance.]

## Skill Version(s):

2.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
