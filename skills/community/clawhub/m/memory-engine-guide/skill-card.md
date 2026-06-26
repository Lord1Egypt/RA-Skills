## Description: <br>
MemGPT-style persistent memory with passive auto-capture that gives an agent long-term recall through core identity, archival facts, knowledge graph relations, episodic summaries, and behavioral reflection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ytangguo](https://clawhub.ai/user/ytangguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they want an OpenClaw agent to retain, search, and manage long-term memory across conversations. It supports recall of prior facts, graph relations, episodes, identity notes, dashboards, imports, exports, and quality maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill persistently stores essentially every conversation and has an always-on long-term memory posture. <br>
Mitigation: Install only when persistent cross-conversation memory is intended, and define retention, deletion, export, and sensitive-topic exclusion practices before use. <br>
Risk: The security evidence flags background behavior and insufficient scoping, consent, retention, or disable guidance. <br>
Mitigation: Before running setup, review the external plugin and setup script, confirm where data is stored, and document how to pause or remove hooks and maintenance crons. <br>
Risk: The artifact describes passive hooks that capture user and agent messages automatically. <br>
Mitigation: Inform users before enabling passive capture and verify that cross-agent sharing is disabled or appropriately scoped for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ytangguo/memory-engine-guide) <br>
- [npm package @icex-labs/openclaw-memory-engine](https://www.npmjs.com/package/@icex-labs/openclaw-memory-engine) <br>
- [GitHub repository icex-labs/openclaw-memory-engine](https://github.com/icex-labs/openclaw-memory-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and tool names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can guide setup and use of memory tools, hooks, dashboards, backup, import, export, and maintenance workflows.] <br>

## Skill Version(s): <br>
5.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
