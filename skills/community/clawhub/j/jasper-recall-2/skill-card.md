## Description: <br>
Local RAG memory system for AI agents using ChromaDB and SkillBoss API Hub embeddings, enabling context recall, continuous learning, and multi-agent shared memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Jasper Recall to index local notes, session logs, and shared memory files so agents can retrieve relevant context across sessions and multi-agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can index and persist local notes, session logs, and private memory in ChromaDB. <br>
Mitigation: Review what paths are indexed, run privacy checks before sharing, and avoid indexing secrets or sensitive sessions. <br>
Risk: Memory text and search queries are sent to SkillBoss API Hub for embeddings. <br>
Mitigation: Install only when this remote embedding flow is acceptable for the data being indexed and queried. <br>
Risk: Automatically injected recall context can expose private memories in untrusted or sandboxed workflows. <br>
Mitigation: Keep autoRecall disabled unless needed, or set publicOnly true and review openclaw.json after setup. <br>
Risk: The HTTP recall server can expose memory search if bound to a public interface. <br>
Mitigation: Keep the server on localhost and do not run it on a public interface. <br>
Risk: Security evidence reports command-injection risks. <br>
Mitigation: Do not index secrets or sensitive sessions until the shell-injection issues are fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/jasper-recall-2) <br>
- [Multi-Agent Mesh guide](docs/MULTI-AGENT-MESH.md) <br>
- [Shared Memory Specification](docs/SHARED-MEMORY-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit recall results as JSON when the documented --json option is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
