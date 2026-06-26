## Description: <br>
Complete memory system with factor inference, genetic neurons, causal graph, knowledge graph, auto-detection, and evolution features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[717986230](https://clawhub.ai/user/717986230) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add a local persistent memory system with SQLite storage, optional vector search, causal and knowledge graph relations, factor inference, and genetic-neuron style memory workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and maintain a local persistent memory database that may contain sensitive user or agent context. <br>
Mitigation: Use it only for data you are prepared to store locally, avoid storing secrets unless you add retention and access controls, and back up the database before verification or relation-detection workflows. <br>
Risk: Optional embedding workflows can process memory content through an Ollama service. <br>
Mitigation: Keep Ollama configured to localhost for sensitive data and review model/service configuration before using semantic search. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/717986230/memory-system-complete) <br>
- [Ollama](https://ollama.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and operates a local persistent memory database when its setup and runtime scripts are used.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and package.json; artifact SKILL.md frontmatter still lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
