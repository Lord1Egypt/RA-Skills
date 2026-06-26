## Description: <br>
OpenClaw 3.8+ intelligent context management and memory system plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lizhelong0907](https://clawhub.ai/user/lizhelong0907) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this plugin to persist local conversation memories, retrieve relevant memories during later turns, and inspect memory statistics through OpenClaw tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can automatically store and later reuse conversation details in persistent local memory. <br>
Mitigation: Use it only when persistent memory is intended, confirm the SQLite database location before handling private data, and review saved entries regularly. <br>
Risk: Sensitive or regulated information may be retained with limited built-in controls for scope and deletion. <br>
Mitigation: Verify OpenClaw access controls for memory listing, confirm whether automatic memory writing can be disabled, and avoid use with regulated data until deletion and retention procedures are clear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lizhelong0907/memory-engine) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lizhelong0907) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration] <br>
**Output Format:** [Text and JSON tool results with configuration fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists and recalls local SQLite-backed memories; the default configured database path is ~/.openclaw/memory/memories.db.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata; artifact frontmatter and package.json report 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
