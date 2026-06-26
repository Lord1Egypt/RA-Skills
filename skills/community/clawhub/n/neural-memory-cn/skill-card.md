## Description: <br>
Neural Memory CN provides a neural-network-inspired memory system with activation spreading, associative retrieval, local operation by default, and optional LLM-based intent analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunlight-Bulling](https://clawhub.ai/user/Sunlight-Bulling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add persistent local knowledge memory, associative retrieval, and optional intent analysis to OpenClaw workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist personal profile, preference, or proprietary memory content in local plaintext files. <br>
Mitigation: Store only information appropriate for local plaintext persistence and periodically review or delete the generated memory directory. <br>
Risk: When LLM integration is enabled or provider API keys are present, queries or memory-derived text may be sent to an external AI provider. <br>
Mitigation: Use local-only mode by default and enable LLM settings only in environments where provider data handling is acceptable. <br>
Risk: The server security review marked the release suspicious because it needs review before installation. <br>
Mitigation: Review the skill source, configuration, and local storage behavior before deployment. <br>


## Reference(s): <br>
- [Neural Memory API Reference](references/api.md) <br>
- [Neural Memory Architecture](references/architecture.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Sunlight-Bulling/neural-memory-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with Python examples, shell commands, YAML configuration, and JSON-like API result structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory files and retrieval results; optional LLM configuration can affect whether query or memory-derived text is sent to an external provider.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
