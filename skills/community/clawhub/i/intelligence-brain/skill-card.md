## Description: <br>
Intelligence Brain helps an agent ingest company reports, external signals, and operational events, convert them into structured intelligence, and produce cross-file inferences, priority actions, and knowledge graph updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ygq19901001](https://clawhub.ai/user/ygq19901001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and agent developers use this skill to turn daily company outputs and external signals into routed intelligence, decision support, and follow-up action items. It is intended for company-intelligence workflows that need classification-aware routing, heartbeat checks, and cross-file inference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic ingestion and routing can expose business data to models or cloud documents that are not approved for the data classification. <br>
Mitigation: Use the skill only in workspaces with explicit data-access permission, enforce the classification routing rules, and keep top-secret data on local processing paths. <br>
Risk: Cleanup behavior can delete raw or parsed business files before retention and review requirements are satisfied. <br>
Mitigation: Gate or disable automatic deletion until retention policy, approvals, and recovery procedures are configured. <br>
Risk: Cloud mirroring and multi-channel communication can broaden the access surface for operational messages and intelligence outputs. <br>
Mitigation: Disable cloud mirroring by default and enable it only after access controls, audit logging, and allowed-destination rules are reviewed. <br>


## Reference(s): <br>
- [8-Step Metabolic Pipeline Operations Playbook](references/pipeline-playbook.md) <br>
- [Cross-File Inference Patterns](references/inference-patterns.md) <br>
- [Neural Chain Design](references/neural-chain-design.md) <br>
- [ClawHub skill page](https://clawhub.ai/ygq19901001/skills/intelligence-brain) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown files and structured Markdown or YAML-style snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces WISDOM_GRAPH nodes, ACTION_PIPELINE priority items, ONE_MORE_THING inferences, classification routing guidance, heartbeat checks, and cleanup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
