## Description: <br>
Maintain Clawdbot's compounding knowledge graph under life/areas/** by adding or superseding atomic facts, regenerating entity summaries, and keeping IDs consistent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SafaTinaztepe](https://clawhub.ai/user/SafaTinaztepe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain Clawdbot's local knowledge graph by adding, superseding, and summarizing facts without manual JSON edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect, sensitive, or untrusted claims could be written into persistent knowledge files. <br>
Mitigation: Review facts before adding or superseding them, and avoid storing sensitive or untrusted claims. <br>
Risk: The skill needs local file read/write access to maintain files under life/areas/**. <br>
Mitigation: Install it only in workspaces where the agent is expected to maintain that knowledge graph, and review resulting file changes before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SafaTinaztepe/knowledge-graph) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands] <br>
**Output Format:** [Markdown instructions with shell commands; script output is plain text and file updates are JSON or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or updates knowledge graph files under life/areas/** when invoked as documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
