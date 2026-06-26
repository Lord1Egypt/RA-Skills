## Description: <br>
Semantic memory plugin using m3e-large embeddings with SQLite storage, supporting storage, retrieval, and deletion via cosine similarity search in pure JavaScript. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalalxy](https://clawhub.ai/user/kalalxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this plugin to give an OpenClaw agent persistent semantic memory backed by a configured m3e-large embedding service and local SQLite storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved memories and search queries are sent to the configured embedding service. <br>
Mitigation: Use HTTPS or a trusted local/self-hosted embedding endpoint and avoid storing secrets or regulated data. <br>
Risk: Persistent memories are stored locally in SQLite. <br>
Mitigation: Keep the database path protected and install only when persistent semantic memory is intended. <br>
Risk: Semantic deletion by broad query may remove an unintended memory. <br>
Mitigation: Prefer deleting by exact memory ID when possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kalalxy/memory-m3e) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [Tool responses with text content and structured details objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores memory text and embedding vectors in a local SQLite database and sends stored or queried text to the configured embedding endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and plugin manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
