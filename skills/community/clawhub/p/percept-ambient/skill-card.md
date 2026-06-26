## Description: <br>
Percept Ambient continuously captures and summarizes ambient conversations to build a local knowledge graph for context-aware assistance without explicit commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarvis563](https://clawhub.ai/user/jarvis563) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill when they want always-on local conversation memory that can assemble searchable context packets about people, projects, decisions, and recent discussions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can continuously capture, store, search, and re-surface sensitive speech from users and bystanders. <br>
Mitigation: Enable it only with clear consent, visible microphone indicators, reviewed retention defaults, and working deletion/export controls. <br>
Risk: Stored transcripts, embeddings, and the localhost dashboard/API may expose sensitive conversation history if they leave the machine or are reachable by untrusted clients. <br>
Mitigation: Confirm embeddings remain local or are explicitly approved, and ensure the dashboard/API is protected and bound only to trusted local access. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jarvis563/percept-ambient) <br>
- [Publisher profile](https://clawhub.ai/user/jarvis563) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON context packet examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can describe local search, dashboard, retention, and privacy-control workflows for ambient conversation context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
