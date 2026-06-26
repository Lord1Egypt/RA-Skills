## Description: <br>
Continuous self-improvement through systematic logging, pattern detection, and behavioral updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to help an agent log corrections, failures, recurring patterns, feature requests, and positive signals, then review those records and promote repeated lessons into operating guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent self-modification can add incorrect or unsafe operating rules. <br>
Mitigation: Require manual review before any write outside .learnings and before promoting changes into SOUL.md, AGENTS.md, TOOLS.md, MEMORY.md, or HEARTBEAT.md. <br>
Risk: Learning logs and memory files can capture private or sensitive context. <br>
Mitigation: Do not store passwords, tokens, cookies, or credentials, and periodically review or delete logs that contain sensitive information. <br>


## Reference(s): <br>
- [Jarvis learning article](https://jarvis.ripper234.com/learn.html) <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/heleni-self-learning) <br>
- [Publisher profile](https://clawhub.ai/user/netanel-abergel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and markdown templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or propose updates to .learnings files and agent operating instructions when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
