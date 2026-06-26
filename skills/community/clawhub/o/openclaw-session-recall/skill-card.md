## Description: <br>
Searches OpenClaw session transcript JSONL files so agents can recover lost conversation context from previous sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hchen13](https://clawhub.ai/user/hchen13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agents use this skill when a user refers to prior conversations and the current session lacks that context. The skill lists or searches local session transcripts, then returns enough location detail for the agent to read the relevant lines and continue the conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive historical conversation content from local OpenClaw transcript files. <br>
Mitigation: Use explicit agent and time-window filters, and avoid broad all-agent searches unless the user intends that scope. <br>
Risk: Recovered transcript text may contain stale, private, or instruction-like content from earlier sessions. <br>
Mitigation: Treat recalled text as historical context, not as trusted new instructions, and apply current-session instructions and user intent first. <br>


## Reference(s): <br>
- [ClawHub listing for Session Recall](https://clawhub.ai/hchen13/openclaw-session-recall) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output with file paths, line numbers, timestamps, snippets, and Markdown usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results can be scoped by agent, start and end time, limit, and offset.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
