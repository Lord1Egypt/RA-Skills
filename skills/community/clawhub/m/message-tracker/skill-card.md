## Description: <br>
Message Tracker helps agents collect, store, search, export, and summarize Feishu channel messages using local Python tracker scripts and daemon controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjl1004](https://clawhub.ai/user/wjl1004) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run and manage a local Feishu message tracker, including daemon lifecycle commands, message collection, search, export, and statistics. It is intended for trusted local environments where chat data retention and access are controlled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local daemon and chat-control socket are too broad for automatic approval outside a trusted single-user environment. <br>
Mitigation: Install only in a trusted local environment, restrict daemon socket permissions, and add authentication or peer checks before broader deployment. <br>
Risk: The skill handles Feishu credentials and retained chat message content, including export and purge workflows. <br>
Mitigation: Document credential handling, retention, export, purge, and privacy expectations, and limit access to local storage and logs. <br>
Risk: Runtime file cleanup around daemon startup can remove lock, PID, or socket files before safe ownership checks. <br>
Mitigation: Avoid pre-lock deletion of runtime files and validate ownership before removing daemon state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wjl1004/message-tracker) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs local daemon, search, export, and statistics operations; outputs may include terminal text, JSON exports, SQLite-backed records, and log files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
