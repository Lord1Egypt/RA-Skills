## Description: <br>
Typed knowledge graph for structured agent memory, entity CRUD, relation queries, schema validation, auto-sync from memory files, and backup memory fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to store, query, validate, and link structured memory entities for projects, tasks, people, documents, events, and cross-skill state. It also supports backup memory workflows when primary memory retrieval fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auto-sync can persist local memory-derived records, installed skill inventory, and hard-coded person, organization, and business records into the ontology graph. <br>
Mitigation: Run ontology_sync.py --dry-run first, inspect the pending writes, and configure the recommended cron job only if persistent local memory writes are intended. <br>
Risk: The sync workflow reads local memory files to populate graph entities and relations. <br>
Mitigation: Use it only in workspaces where those memory files are appropriate for structured indexing, and review the generated graph before relying on it. <br>


## Reference(s): <br>
- [Schema reference](references/schema.md) <br>
- [Query reference](references/queries.md) <br>
- [ClawHub release page](https://clawhub.ai/paudyyin/ontology-knowledge-graph) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON, YAML, Python, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local JSONL graph records and YAML schema files when its scripts are run.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
