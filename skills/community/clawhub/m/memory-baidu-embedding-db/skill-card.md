## Description: <br>
Semantic memory system using Baidu Embedding-V1 for vector-based memory storage and retrieval in Clawdbot with SQLite persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xqicxx](https://clawhub.ai/user/xqicxx) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Clawdbot operators use this skill to store, retrieve, and search conversational or knowledge memories by semantic similarity using Baidu embeddings and local SQLite storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory content and search queries may be sent to Baidu for embedding despite local-storage privacy claims. <br>
Mitigation: Avoid storing secrets or sensitive personal data, disclose external embedding processing to users, and use approved Baidu credentials only for data appropriate for that service. <br>
Risk: The skill depends on an external baidu-vector-db helper located outside the artifact. <br>
Mitigation: Inspect and pin the helper before installation, and verify its source and behavior before enabling Baidu-backed embeddings. <br>
Risk: Maintenance and disable instructions can modify /root/clawd files, backups, symlinks, or Clawdbot extension directories. <br>
Mitigation: Review each command before execution, run with the least privileges needed, and back up affected Clawdbot memory and configuration files first. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xqicxx/memory-baidu-embedding-db) <br>
- [Baidu Qianfan Console](https://console.bce.baidu.com/qianfan/) <br>
- [README](README.md) <br>
- [API Reference](API_REFERENCE.md) <br>
- [Security Configuration](SECURITY_CONFIG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and bash examples; runtime memory APIs return JSON-like dictionaries and lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores memory text, tags, metadata, and embeddings in SQLite; Baidu-backed embedding calls require BAIDU_API_STRING and BAIDU_SECRET_KEY.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
