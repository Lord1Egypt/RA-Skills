## Description:

Query New Relic observability data and manage approved deployment, NRQL macro, dataset, diagnostic, and identity and access workflows with the New Relic CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vince-winkintel](https://clawhub.ai/user/vince-winkintel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site reliability engineers use this skill to inspect New Relic telemetry, troubleshoot application and host performance, review incidents, and carry out approved operational changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because of broad activation triggers and guidance for potentially disruptive or persistent changes; the scan was partial and its tool-poisoning analysis was degraded.

Mitigation: Review activation scope and skill content before installation, and use it only for relevant New Relic tasks.

Risk: Some workflows can change profiles, restart services, or make organization-wide changes.

Mitigation: Require explicit approval for the exact target and scope, use the minimum required access, and verify changes by reading the target back.

## Reference(s):

- [CLI installation and checksum verification](references/installation.md)
- [NRQL patterns reference](references/nrql-patterns.md)
- [Performance triage guide](references/performance-triage.md)
- [AI Monitoring datasets and versions](aimonitoring/references/datasets.md)
- [CLI configuration validation and safeguards](diagnostics/references/config-validation.md)
- [New Relic NRQL macro documentation](https://docs.newrelic.com/docs/nrql/nrql-macros/create-manage-nrql-macros/)
- [New Relic CLI release list](https://github.com/newrelic/newrelic-cli/releases)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands, NRQL examples, and result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content depends on the requested New Relic task and the account data available.]

## Skill Version(s):

1.0.13 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
