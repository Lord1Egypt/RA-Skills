## Description: <br>
Builds a typed knowledge graph for AI agents with entities, relationships, constraint validation, and JSONL storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, project managers, and automation teams use this skill to structure project knowledge, tasks, people, documents, and dependencies as a typed local graph that an agent can create, query, validate, and update. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or append graph files in the workspace. <br>
Mitigation: Review existing memory/knowledge-graph files before append operations and keep backups or version control for important graphs. <br>
Risk: Graph entries may accidentally include passwords, tokens, or other secrets. <br>
Mitigation: Use references for credentials instead of storing secret values directly, and review graph entries before committing or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/knowledge-graph-builder-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSONL, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or append local files under memory/knowledge-graph when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
