## Description: <br>
Local retrieval-augmented generation system for AI agents using ChromaDB and sentence-transformers, supporting multi-agent shared memory and privacy controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emberDesire](https://clawhub.ai/user/emberDesire) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use Jasper Recall to index local memory files and session digests, then retrieve relevant prior context through CLI commands, JSON output, or an optional local recall server. It also supports public-only shared memory workflows for sandboxed or lower-trust agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored memories may contain private or sensitive local data that can be surfaced in responses. <br>
Mitigation: Keep autoRecall disabled unless automatic memory insertion is intended, review memories before sharing, and use publicOnly for sandboxed or lower-trust agents. <br>
Risk: The local recall server can expose memory search over HTTP if it is bound beyond localhost or private queries are enabled. <br>
Mitigation: Keep the server on localhost, avoid enabling private HTTP queries on shared hosts, and do not expose the service externally without additional controls. <br>
Risk: The ChromaDB database, legacy collection, session digests, and shared learnings are sensitive local data stores. <br>
Mitigation: Treat these files as sensitive, restrict file permissions, and review retention or sharing workflows before deployment. <br>
Risk: Security evidence reports that some query paths invoke shell commands unsafely. <br>
Mitigation: Review the implementation before installation, constrain input sources, and run the skill in a sandboxed or dedicated account when possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/emberDesire/jasper-recall) <br>
- [Jasper Recall README](artifact/README.md) <br>
- [Multi-Agent Mesh Documentation](artifact/docs/MULTI-AGENT-MESH.md) <br>
- [Shared Memory Specification](artifact/docs/SHARED-MEMORY-SPEC.md) <br>
- [npm Package](https://www.npmjs.com/package/jasper-recall) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus text or JSON recall results from the tool.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local markdown digests, ChromaDB indexes, shared-memory files, plugin configuration, and local server responses depending on the command used.] <br>

## Skill Version(s): <br>
0.4.0 (source: evidence.release.version and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
