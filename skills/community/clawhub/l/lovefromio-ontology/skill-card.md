## Description: <br>
Typed knowledge graph for structured agent memory and composable skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovefromio](https://clawhub.ai/user/lovefromio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create, query, link, and validate typed workspace entities such as people, projects, tasks, events, and documents. It supports shared local memory and graph-based planning across skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores persistent local workspace memory that other local tools or skills may read or reuse. <br>
Mitigation: Install it only when shared local memory is intended, and avoid storing raw secrets, private message contents, or sensitive account details. <br>
Risk: Publisher and source provenance may matter in controlled environments, and server-resolved GitHub provenance is unavailable for this release. <br>
Mitigation: Verify the lovefromio publisher profile, release version, and artifact hashes before deployment. <br>
Risk: Some higher-level ontology constraints may be documentation-only unless implemented in code. <br>
Mitigation: Run validation after ontology changes and review schema-dependent behavior before relying on it for enforcement. <br>


## Reference(s): <br>
- [Ontology Schema Reference](references/schema.md) <br>
- [Query Reference](references/queries.md) <br>
- [ClawHub skill page](https://clawhub.ai/lovefromio/lovefromio-ontology) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lovefromio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON, YAML, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reads local workspace ontology files under memory/ontology when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
