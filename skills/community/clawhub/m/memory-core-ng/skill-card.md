## Description: <br>
A modular intelligent memory system for embeddings, reranking, semantic search, and Flomo note integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jazzqi](https://clawhub.ai/user/jazzqi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add, search, rank, and manage semantic memories, with optional import of Flomo notes into the memory store. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact ships a hardcoded API key in its configuration template. <br>
Mitigation: Remove or rotate the bundled key before use and configure credentials through an approved secret or environment variable path. <br>
Risk: Memory contents, search queries, and imported notes may be sent to Edgefn or another configured provider. <br>
Mitigation: Avoid importing secrets or regulated personal data unless the configured provider is approved for that data. <br>
Risk: Smart Memory integration can affect existing memories if enabled without review. <br>
Mitigation: Review the migration path and test on non-production memory data before enabling integration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jazzqi/memory-core-ng) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>
- [Configuration template](artifact/config/template.json) <br>
- [Package metadata](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, code] <br>
**Output Format:** [OpenClaw command responses and JavaScript API results, with JSON configuration for setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and import behavior depends on the configured embedding, rerank, Flomo, and storage settings.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact package.json declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
