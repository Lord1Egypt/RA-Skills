## Description: <br>
Helps agents maintain local memory through write-ahead session notes, a working buffer, context budget zones, and HOT/WARM/COLD memory tiering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silaszhu](https://clawhub.ai/user/silaszhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to structure persistent local memory for long-running OpenClaw sessions, including session state, learning logs, checkpoints, and archived context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists conversation details, decisions, preferences, and working context in local memory files. <br>
Mitigation: Use it only when persistent local memory is intended, avoid secrets or confidential data, and add redaction, retention, and deletion controls for sensitive environments. <br>
Risk: Initialization and tiering scripts can create, reset, archive, or overwrite active memory files such as SESSION-STATE.md, memory/, and .learnings/. <br>
Mitigation: Back up those paths before running init.sh or tiering.sh and review the configured OpenClaw workspace before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/silaszhu/proactive-memory-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and local file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local memory files under the configured OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
