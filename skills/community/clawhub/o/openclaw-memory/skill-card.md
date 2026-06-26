## Description: <br>
Persistent, locally stored semantic memory for agents with automatic learning, searchable facts, and optional paid unlimited retention across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to persist user preferences, project facts, conversation context, and reusable patterns across OpenClaw sessions with semantic search and optional memory injection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can capture and reuse sensitive prompt and response content. <br>
Mitigation: Enable the skill only for workspaces where persistent local memory is acceptable, review stored memories periodically, and avoid storing secrets or regulated data. <br>
Risk: The dashboard and memory/payment APIs are described as unauthenticated. <br>
Mitigation: Run the dashboard on a trusted local-only interface, avoid exposing it to shared networks, or add authentication before broader deployment. <br>
Risk: OpenAI embeddings may send conversation-derived text to an external API. <br>
Mitigation: Use the local embedding provider unless external processing is explicitly approved for the data being stored. <br>
Risk: Agent-initiated x402 payments can spend funds without direct human approval. <br>
Mitigation: Do not give agents funded wallets or autonomous spending authority unless strict limits and operator review are in place. <br>
Risk: Pro activation is insecure until real on-chain payment verification is implemented. <br>
Mitigation: Treat Pro payment verification as untrusted and rely on free-tier behavior unless payment verification is independently hardened. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AtlasPA/openclaw-memory) <br>
- [Agent Payments Guide](AGENT-PAYMENTS.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, CLI examples, REST API examples, and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill stores and retrieves local SQLite-backed memory records and may inject relevant memories into agent requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
