## Description: <br>
Generate an interactive HTML viewer for OpenClaw conversation sessions, including full conversation history, tool calls, tool results, token usage, and debugging details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nan-wang](https://clawhub.ai/user/nan-wang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review, analyze, and debug OpenClaw conversation sessions, including context flow, tool activity, and token usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML or JSON exports can expose complete OpenClaw session contents, including user messages, tool outputs, and debugging details. <br>
Mitigation: Choose a private output path, review exports before sharing, and delete generated files when they are no longer needed. <br>
Risk: Broad trigger phrases may cause the skill to be used when a lightweight conversation summary would be less sensitive. <br>
Mitigation: Invoke the skill only when a full local session export is intentionally needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nan-wang/openclaw-session-viewer) <br>
- [Publisher Profile](https://clawhub.ai/user/nan-wang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated artifacts are HTML or JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated viewer may contain complete local session logs, tool outputs, and debugging details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
