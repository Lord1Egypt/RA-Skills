## Description: <br>
Typed knowledge graph for structured agent memory and composable skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonydesign1999](https://clawhub.ai/user/tonydesign1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain structured local memory, query typed entities, link related objects, validate graph constraints, and share state across compatible skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent graph data can retain personal, project, account, or operational memory across future agent sessions. <br>
Mitigation: Review memory/ontology periodically and store only data intended for persistent local memory. <br>
Risk: Credential-like entities could accidentally capture raw passwords, tokens, keys, or secrets. <br>
Mitigation: Use secret_ref or credential_ref values instead of raw secrets, matching the skill guidance and schema examples. <br>
Risk: Delete and schema-append operations can change shared memory behavior for future workflows. <br>
Mitigation: Review proposed graph and schema mutations before execution, especially operations that remove entities or alter constraints. <br>


## Reference(s): <br>
- [Schema Reference](references/schema.md) <br>
- [Query Reference](references/queries.md) <br>
- [ClawHub release page](https://clawhub.ai/tonydesign1999/ontology-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON, YAML, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local JSONL graph data and YAML schema files under memory/ontology when used.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
