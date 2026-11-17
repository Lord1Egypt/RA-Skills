## Description:

Intelligence Brain helps an agent ingest company signals, structure them into facts, connect related evidence across files, route information by sensitivity, and produce decision-oriented intelligence outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ygq19901001](https://clawhub.ai/user/ygq19901001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to turn daily reports, shared messages, external signals, and system events into structured intelligence, prioritized action items, and cross-file inferences. It is intended for company knowledge workflows that need classification-aware routing and recurring health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive company information may be routed to external models or cloud storage.

Mitigation: Require local pre-classification before any external model call, disable cloud mirroring for sensitive messages, and limit approved sources and recipients.

Risk: Automatic deletion workflows may remove source data before retention and audit requirements are satisfied.

Mitigation: Define explicit approval, retention, recovery, and audit policies before enabling cleanup or background heartbeat workflows.

Risk: Cross-file inferences and priority recommendations may be wrong or overconfident when based on incomplete or conflicting source material.

Mitigation: Require confidence labels, contradiction handling, and human review for unresolved conflicts or high-impact actions.

## Reference(s):

- [8-Step Metabolic Pipeline Operations Playbook](references/pipeline-playbook.md)
- [Cross-File Inference Patterns](references/inference-patterns.md)
- [Neural Chain Design](references/neural-chain-design.md)
- [ClawHub Skill Page](https://clawhub.ai/ygq19901001/skills/intelligence-brain)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured examples for intelligence graphs, action pipelines, routing rules, and operational checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected outputs include WISDOM_GRAPH nodes, ACTION_PIPELINE priorities, ONE_MORE_THING inferences, classification routing decisions, health checks, and cleanup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 1.5.0 and release changelog says v1.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
