## Description: <br>
Local semantic memory with Qdrant and Transformers.js. Store, search, and recall conversation context using vector embeddings (fully local, no API keys). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuiho-kai](https://clawhub.ai/user/zuiho-kai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to give an agent semantic memory across conversations, including storing facts, searching prior context, and deleting remembered entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store conversation content as agent memory, and enabling automatic capture may save sensitive or personal information. <br>
Mitigation: Keep autoCapture disabled unless memory capture is explicitly desired, avoid storing secrets, and periodically review or delete stored memories. <br>
Risk: Using an external Qdrant server sends memory data to that configured service. <br>
Mitigation: Use the default in-memory mode for sensitive data or connect only to a trusted Qdrant server with appropriate access controls. <br>
Risk: The first run downloads an embedding model from Hugging Face. <br>
Mitigation: Allow the download only in environments where that network access is expected, or pre-stage dependencies according to the deployment process. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zuiho-kai/memory-qdrant) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/zuiho-kai) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Tool results and concise configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Memory search returns relevant stored text; memory deletion returns status information.] <br>

## Skill Version(s): <br>
1.0.10 (source: frontmatter, package.json, CHANGELOG, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
