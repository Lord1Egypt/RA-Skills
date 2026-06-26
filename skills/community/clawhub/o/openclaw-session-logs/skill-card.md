## Description: <br>
Search and analyze your own session logs (older/parent conversations) using jq. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronmda](https://clawhub.ai/user/aaronmda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and support engineers use this skill to locate, inspect, and summarize prior local session JSONL logs when current conversation context is incomplete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to search local OpenClaw conversation history, which may expose sensitive personal details or secrets from prior chats. <br>
Mitigation: Ask for specific dates, sessions, or keywords when possible, and avoid returning secrets or sensitive personal details unless the user explicitly needs them. <br>


## Reference(s): <br>
- [OpenClaw Session Logs ClawHub page](https://clawhub.ai/aaronmda/openclaw-session-logs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash and jq command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only guidance for querying local OpenClaw session JSONL files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
