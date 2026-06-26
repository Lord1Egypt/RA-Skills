## Description: <br>
Instantly switch the current OpenClaw session model; supports gpt, claude, qianwen, minimax, current model status, configured model listing, and restoring the default session model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dpbs-715](https://clawhub.ai/user/dpbs-715) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to switch, reset, inspect, or list the model for the current OpenClaw session without editing global configuration or restarting the Gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change the active model for the current OpenClaw session. <br>
Mitigation: Install and use it only when session-level model switching is intended, and confirm switches affect only the current session. <br>
Risk: The handler relies on local OpenClaw helper scripts outside the reviewed package. <br>
Mitigation: Before use, verify those local helper scripts are the expected OpenClaw model switching, status, and listing helpers and do not perform unrelated actions. <br>


## Reference(s): <br>
- [OpenClaw Session Model Switcher on ClawHub](https://clawhub.ai/dpbs-715/openclaw-session-model-switcher) <br>
- [Publisher profile](https://clawhub.ai/user/dpbs-715) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline session model commands and candidate lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May output direct /model commands, status guidance, grouped configured-model lists, or ambiguity prompts.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
