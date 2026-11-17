## Description:

Monitor, query, and manage New Relic observability data through the newrelic CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vince-winkintel](https://clawhub.ai/user/vince-winkintel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site reliability engineers use this skill to inspect New Relic telemetry, investigate application and infrastructure health, and perform targeted deployment, NRQL macro, IAM, or diagnostic workflows through the New Relic CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a suspicious verdict due to possible alert-scope guidance concerns and incomplete analysis; the available scan does not establish malicious intent.

Mitigation: Consider delaying installation until the alert-condition guidance is clarified and the partially inspected material has been reviewed.

## Reference(s):

- [NRQL query patterns](references/nrql-patterns.md)
- [Performance triage guide](references/performance-triage.md)
- [Configuration validation safeguards](diagnostics/references/config-validation.md)
- [New Relic CLI releases](https://github.com/newrelic/newrelic-cli/releases)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and JSON CLI output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and queries use the user's selected New Relic account and requested entities, time ranges, and filters.]

## Skill Version(s):

1.0.11 (source: frontmatter, VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
