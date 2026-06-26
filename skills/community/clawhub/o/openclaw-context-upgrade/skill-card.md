## Description: <br>
Diagnose and upgrade OpenClaw conversation context limits, especially moving a chat from ~272k to 1M. Use when the user asks to enlarge context, make GPT-5.4 use 1M context, change `agents.defaults.contextTokens`, verify why a chat still shows 272k after changes, or execute the full workflow of model selection + config patch + restart + fresh session + status verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juan-xin-cai](https://clawhub.ai/user/juan-xin-cai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose OpenClaw context capacity and guide a configuration change toward a 1M-token conversation budget. It covers model selection, context-token defaults, restart behavior, fresh-session verification, and common failure modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Changing OpenClaw defaults can trigger a restart and persistently alter the context budget for future sessions. <br>
Mitigation: Confirm the user wants the change before patching, include a clear restart note, and verify the setting with a fresh session. <br>
Risk: A requested 1M-token budget may not be available if the selected model, provider, or existing chat session keeps a lower real limit. <br>
Mitigation: Pin or verify the high-context model, start a new or reset chat, and report provider caps plainly when status still shows a lower limit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juan-xin-cai/openclaw-context-upgrade) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline command and configuration names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include diagnostic steps, config patch guidance, restart notes, and verification checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
