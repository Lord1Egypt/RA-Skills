## Description: <br>
Universal memory architecture for AI agents. Provides long-term memory, daily logs, diary, cron inbox, heartbeat state tracking, social platform post tracking, sub-agent context patterns, and adaptive learning -- everything an agent needs for identity continuity across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PsychoTechV4](https://clawhub.ai/user/PsychoTechV4) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to give agents persistent file-based memory across sessions, including long-term notes, daily logs, a cron inbox, heartbeat state, diary entries, platform post tracking, and strategy notes. It is useful when an agent needs continuity, cross-session coordination, and periodic memory maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files can accumulate sensitive personal, operational, or account-related information over time. <br>
Mitigation: Keep secrets such as API keys, passwords, tokens, recovery codes, and precise secret locations out of memory files; restrict workspace access and periodically review or delete old entries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PsychoTechV4/jarvis-memory-architecture) <br>
- [Publisher profile](https://clawhub.ai/user/PsychoTechV4) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Memory template](artifact/templates/MEMORY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and JSON or Markdown templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local file-based memory structure that may contain sensitive persistent records and should be reviewed periodically.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
