## Description: <br>
Local semantic memory with Qdrant and Transformers.js. Store, search, and recall conversation context using vector embeddings (fully local, no API keys). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuiho-kai](https://clawhub.ai/user/zuiho-kai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and OpenClaw users use this plugin to give agents long-term semantic memory for storing, searching, forgetting, and auto-recalling conversation context with local embeddings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-term memory can retain sensitive conversation content, including PII if autoCapture and allowPIICapture are enabled. <br>
Mitigation: Leave autoCapture and allowPIICapture off in sensitive or shared environments, and review stored memories regularly. <br>
Risk: Disk persistence can keep memories on the local filesystem beyond the current agent session. <br>
Mitigation: Set persistToDisk to false for volatile memory, or choose and protect an appropriate storagePath. <br>
Risk: Configuring qdrantUrl can send memory data to an external Qdrant server. <br>
Mitigation: Use only trusted Qdrant servers and avoid external storage for sensitive memory data unless the deployment has appropriate controls. <br>
Risk: First run downloads an embedding model from Hugging Face. <br>
Mitigation: Install only in environments where this network access is acceptable, and prepare dependencies before deployment in restricted networks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zuiho-kai/openclaw-memory-qdrant) <br>
- [Project homepage from artifact metadata](https://github.com/zuiho-kai/openclaw-memory-qdrant) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Text responses and JSON payloads from memory tools, plus configuration examples and shell commands in documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Memory entries may be persisted locally, sent to a configured Qdrant server, or injected as recalled context depending on configuration.] <br>

## Skill Version(s): <br>
1.0.15 (source: SKILL.md frontmatter, package.json, CHANGELOG, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
