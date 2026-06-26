## Description: <br>
Use this skill to read and write a local hybrid memory stack with Postgres facts, Redis realtime state, and Qdrant vector recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VegaBai](https://clawhub.ai/user/VegaBai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an assistant needs durable facts, short-lived state, or semantic recall beyond Markdown memory. It provides guidance and helper scripts for local Postgres, Redis, and Qdrant operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an assistant broad local memory database access, including durable writes and deletes. <br>
Mitigation: Use least-privilege credentials, protect the environment file, prefer read-only use unless persistence is explicitly requested, and confirm update or delete operations. <br>
Risk: Stored facts, Redis state, and vector payloads can become stale, incorrect, or overly broad. <br>
Mitigation: Back up or periodically review stored facts, Redis state, and Qdrant payloads, and use tags, TTLs, and source metadata to support cleanup. <br>


## Reference(s): <br>
- [Hybrid Memory Stack Connections](references/connection-map.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/VegaBai/memory-hybrid-stack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or SQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local database reads, writes, deletes, and Qdrant HTTP calls through bundled helper scripts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
