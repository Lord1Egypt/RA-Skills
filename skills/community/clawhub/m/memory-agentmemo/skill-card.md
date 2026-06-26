## Description: <br>
OpenClaw external memory plugin for AgentMemo that enables semantic memory search and auto-capture via a self-hosted AgentMemo server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yxjsxy](https://clawhub.ai/user/yxjsxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect OpenClaw's memory layer to a self-hosted AgentMemo server for semantic recall and optional memory capture instead of local file-based memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and captured messages can be sent to the configured AgentMemo server. <br>
Mitigation: Install only when you trust and control that server; prefer localhost or a protected HTTPS instance. <br>
Risk: Auto-capture can store conversation-derived memories, including sensitive content if users provide it. <br>
Mitigation: Keep autoCapture disabled unless intentional, and avoid secrets, regulated data, or private conversations without retention and deletion controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yxjsxy/memory-agentmemo) <br>
- [AgentMemo project](https://github.com/yxjsxy/agentMemo) <br>
- [AgentMemo server reference](https://github.com/agentmemo/agentmemo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration, Guidance] <br>
**Output Format:** [Plain text memory snippets with JSON HTTP requests and responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can auto-inject relevant memories into context and optionally store conversation-derived memories when autoCapture is enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
