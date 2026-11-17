## Description:

Ontology provides a typed knowledge graph for structured agent memory and composable skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to model people, projects, tasks, notes, credentials, events, and relationships as validated graph records in local workspace memory. It supports creating, querying, linking, and validating ontology objects for structured recall and cross-skill coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to maintain local structured memory in the workspace, including creating or updating ontology files.

Mitigation: Use explicit requests for writes, review memory/ontology/graph.jsonl and memory/ontology/schema.yaml periodically, and keep ontology changes append-only or merged.

Risk: Ontology records could accidentally include secrets, raw credentials, or sensitive account data.

Mitigation: Store credential references only, avoid raw secrets and tokens, and follow the skill's Credential pattern that uses secret_ref instead of secret values.

Risk: Broad natural-language triggers could lead to unintended memory capture.

Mitigation: Confirm user intent before writing persistent ontology entries and avoid storing information that was not explicitly requested for memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ontology-2)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local workspace ontology files such as memory/ontology/graph.jsonl and memory/ontology/schema.yaml when the agent follows the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
