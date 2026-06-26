## Description: <br>
Interact with IATerm terminals via the local WebSocket API (ws://127.0.0.1:19790/ws). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sutaixu](https://clawhub.ai/user/sutaixu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to discover IATerm workspaces, displays, panels, and remote terminal connections, then send terminal input or subscribe to terminal output through the local WebSocket API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate IATerm terminals, including remote SSH or serial sessions. <br>
Mitigation: Install only when terminal operation is intended and scope target connections carefully. <br>
Risk: Auto-approval or persistent approval choices can bypass per-operation confirmation for sensitive terminal actions. <br>
Mitigation: Avoid --auto-approve and persistent always-approve choices unless the target is tightly bounded; clear ~/.cache/iaterm-ws-client to revoke cached tokens or approvals. <br>
Risk: Interactive JSON mode can send arbitrary WebSocket methods outside the documented command flow. <br>
Mitigation: Review interactive-mode requests carefully before use and prefer documented commands for routine operation. <br>


## Reference(s): <br>
- [IATerm WebSocket Agent on ClawHub](https://clawhub.ai/sutaixu/iaterm-ws-client) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit streamed terminal output during subscriptions.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
