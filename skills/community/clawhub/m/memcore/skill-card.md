## Description: <br>
MemCore provides an enhanced long-term memory system for agents with episodic memory, semantic compression, memory triggers, forgetting-curve cleanup, persistent storage, vector knowledge retrieval, conflict resolution, and confidence tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laojun509](https://clawhub.ai/user/laojun509) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building memory-enabled agents use MemCore to store, retrieve, compress, and manage long-term context such as user preferences, task state, knowledge, and prior decisions across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored memories can contain sensitive user preferences, task state, or knowledge records. <br>
Mitigation: Treat the local ~/.memcore database as sensitive, avoid storing secrets or regulated personal data without additional controls, and apply appropriate access controls and retention policies. <br>
Risk: Forgetting and cleanup methods can delete memory records that may still be useful. <br>
Mitigation: Back up important records before running forgetting or cleanup cycles and review retention settings before deployment. <br>
Risk: The optional OpenAI embedding wrapper can send text to an external provider. <br>
Mitigation: Use the remote embedding path only for text approved for that provider, or keep the default local embedding behavior for sensitive data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [Python modules and Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local SQLite or JSON memory stores when used by an agent application.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and artifact package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
