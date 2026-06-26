## Description: <br>
Heartbeat-Memories is a fully local long-term memory system for OpenClaw with five memory banks, semantic search, and heartbeat recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jamieyang9996](https://clawhub.ai/user/jamieyang9996) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to maintain local long-term memories about goals, technical experience, sessions, versions, and emotional context, then retrieve those memories during later conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and resurfaces personal conversations, goals, habits, and emotional history by default. <br>
Mitigation: Review the configuration before use, disable auto_record or heartbeat_recall if unwanted, and avoid storing secrets or highly sensitive personal information. <br>
Risk: Heartbeat recall can proactively reintroduce remembered personal context during later conversations. <br>
Mitigation: Lower recall probabilities, set stricter frequency limits, or turn heartbeat_recall off when proactive memory resurfacing is not appropriate. <br>
Risk: Reset or uninstall workflows can remove local memory data if users have not backed it up. <br>
Mitigation: Back up the memory directory before running reset, cleanup, or uninstall commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jamieyang9996/heartbeat-memories) <br>
- [Publisher profile](https://clawhub.ai/user/jamieyang9996) <br>
- [Artifact README](artifact/README.md) <br>
- [Installation guide](artifact/docs/installation.md) <br>
- [Configuration template](artifact/config/hbm_config_template.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, code snippets, and configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can create and query local Markdown memory files and a local vector database when installed and initialized.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
