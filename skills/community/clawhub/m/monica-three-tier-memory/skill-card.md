## Description: <br>
Three Tier Memory manages an AI agent's short-term sliding-window memory, medium-term summaries, and long-term retrieval for conversation continuity and persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forvendettaw](https://clawhub.ai/user/forvendettaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to keep local conversation memory across sessions, summarize recent context, and retrieve longer-term memories before or during future conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally stores conversation memories locally, which may include sensitive personal or business data. <br>
Mitigation: Set WORKSPACE_DIR deliberately, avoid storing secrets or sensitive data, and periodically review or delete the memory directory. <br>
Risk: Long-term memory depends on ChromaDB when that feature is used. <br>
Mitigation: Install ChromaDB only from trusted, pinned versions and keep the vector-store directory within the intended workspace. <br>


## Reference(s): <br>
- [Memory Manager Command Reference](references/references.md) <br>
- [ClawHub skill page](https://clawhub.ai/forvendettaw/monica-three-tier-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON/YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local memory files under WORKSPACE_DIR/memory and can use ChromaDB for long-term retrieval when installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
