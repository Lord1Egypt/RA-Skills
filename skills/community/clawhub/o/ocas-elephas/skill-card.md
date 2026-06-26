## Description: <br>
Elephas maintains Chronicle, a long-term knowledge graph that ingests structured journal signals, resolves entity identity, promotes confirmed facts, and supports queries over durable knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigokarasu](https://clawhub.ai/user/indigokarasu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Elephas to query Chronicle, ingest structured signals from skill journals, run consolidation passes, resolve duplicate entities, and promote supported candidates into confirmed long-term facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can register recurring background jobs and a silent self-update that changes the installed package. <br>
Mitigation: Review scheduled jobs before enabling them, disable the self-update cron by default, and require manual approval for package updates. <br>
Risk: The skill reads OpenClaw journals and writes confirmed information into a durable knowledge graph. <br>
Mitigation: Use explicit journal source allowlists, review data scope before installation, and verify promoted facts before relying on them. <br>
Risk: Identity merge and promotion actions can make incorrect or stale information persistent. <br>
Mitigation: Back up Chronicle before merge operations, preserve reversible merge history, and require manual approval for ambiguous identity matches. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/indigokarasu/ocas-elephas) <br>
- [README](README.md) <br>
- [Ingestion Pipeline](references/ingestion_pipeline.md) <br>
- [Elephas Initialization Pattern](references/init_pattern.md) <br>
- [Journal](references/journal.md) <br>
- [Chronicle Ontology](references/ontology.md) <br>
- [Chronicle Schemas](references/schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command names, JSON examples, Cypher examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce journal records, Chronicle queries, consolidation decisions, identity-resolution guidance, and operational commands for an agent to execute.] <br>

## Skill Version(s): <br>
2.3.0 (source: evidence.release.version and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
