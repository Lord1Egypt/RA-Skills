## Description: <br>
Local persistent vector memory system using LanceDB and Ollama for semantic search and multi-user isolated long-term AI assistant memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2830201534](https://clawhub.ai/user/2830201534) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agent users use this skill to give an assistant long-term local memory, semantic recall, recent-memory lookup, deduplication, and private or shared multi-user memory modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic memory hooks can persist sensitive conversation details into long-term local storage. <br>
Mitigation: Enable the hook only when broad conversation capture is intended, and avoid storing secrets or regulated personal data. <br>
Risk: Shared or misconfigured multi-user mode can expose memories beyond the intended user. <br>
Mitigation: Verify OPENCLAW_USER_ID is reliably set and keep private mode unless cross-user sharing is explicitly required. <br>
Risk: Installer scripts and dependency versions may affect deployment trust and reproducibility. <br>
Mitigation: Review the Ollama installer scripts and dependency pinning before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/2830201534/pidan-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Configuration, Shell commands] <br>
**Output Format:** [JSON command responses and text memory summaries, with setup guidance using shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and retrieves local vector memories through LanceDB and Ollama; memory visibility depends on private or shared mode.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
