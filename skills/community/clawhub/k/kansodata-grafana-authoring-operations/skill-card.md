## Description:

Opera Grafana en OpenClaw con enfoque seguro: inspeccion real, diagnostico, propuesta de cambios y aplicacion solo cuando exista tooling habilitado y contexto suficiente.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kansodata](https://clawhub.ai/user/kansodata)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to inspect Grafana health, dashboards, datasources, folders, and alert rules before proposing dashboard JSON or alerting changes. It supports safe review workflows by degrading uncertain changes to drafts and requiring enabled write tooling plus gates before applying changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare dashboard or alerting changes that may be incorrect if Grafana state is stale, partial, or inferred.

Mitigation: Require current read-only inspection before proposals and mark uncertain outputs as draft or human_review_required.

Risk: Write-capable Grafana tools could modify dashboards or alerting resources if exposed without controls.

Mitigation: Expose write tools only for trusted Grafana instances and require enabled tooling, sufficient context, and a human review or gate before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kansodata/skills/kansodata-grafana-authoring-operations)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Grafana dashboard JSON, logical diffs, status labels, and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may be marked draft, review_ready, apply_ready, or human_review_required depending on verified Grafana context and available tooling.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
