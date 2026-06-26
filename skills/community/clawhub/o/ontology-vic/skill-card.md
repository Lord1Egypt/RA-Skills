## Description: <br>
Typed knowledge graph for structured agent memory and composable skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chungvic](https://clawhub.ai/user/chungvic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create, query, relate, and validate typed entities for reusable local memory, dependency tracking, planning, and cross-skill state sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended to keep reusable structured memory in local files, which can expose sensitive personal data or secrets if users store them directly. <br>
Mitigation: Avoid storing plaintext secrets or sensitive personal data; use references such as secret_ref or credential_ref and review the implementation that reads or writes ontology files. <br>
Risk: Broad memory triggers may cause agents to record more information than intended. <br>
Mitigation: Review proposed ontology mutations before committing them and keep memory files scoped to the workspace where the skill is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chungvic/ontology-vic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, JSONL examples, YAML schema examples, and local file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for append-only local storage under memory/ontology and optional schema validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
