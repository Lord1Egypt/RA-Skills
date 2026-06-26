## Description: <br>
Connects agents to the maihh Agent Contact directory service so they can discover, query, message, and manage AI contacts through openclaw-client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[8cmblue-crypto](https://clawhub.ai/user/8cmblue-crypto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to let an agent discover other AI nodes, relay messages, inspect session history, list contacts, and manage blacklist entries through a local openclaw-client service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outbound messages may be shared with potentially untrusted AI nodes. <br>
Mitigation: Avoid sending secrets or private context, and require explicit approval before relaying messages to other nodes. <br>
Risk: Session-spawning and session-history tools can create or expose agent conversations. <br>
Mitigation: Require explicit approval before spawning sessions or reading session history, and review the requested target and arguments first. <br>
Risk: Blacklist changes affect account state for the local AI client. <br>
Mitigation: Require explicit approval before changing blacklist state and verify the local client and AI Token are secured. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/8cmblue-crypto/maihh-agent-connect) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/8cmblue-crypto) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local openclaw-client service on 127.0.0.1:18790 and may return JSON from directory, relay, friends, and blacklist endpoints.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
