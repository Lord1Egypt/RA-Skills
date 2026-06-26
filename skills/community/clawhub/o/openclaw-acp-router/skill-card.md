## Description: <br>
Route plain-language requests for Pi, Claude Code, Codex, OpenCode, Gemini CLI, or ACP harness work into either OpenClaw ACP runtime sessions or direct acpx-driven sessions ("telephone game" flow). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zch-danny](https://clawhub.ai/user/zch-danny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route requests into supported ACP coding harnesses, create or continue harness sessions, and choose between OpenClaw ACP runtime sessions and direct acpx-driven workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary states that the skill can make local software and configuration changes before clearly asking the user. <br>
Mitigation: Require explicit confirmation before any npm install, gateway restart, or change to ~/.acpx/config.json. <br>
Risk: Persistent harness sessions can retain prompts or context that may include sensitive information. <br>
Mitigation: Avoid sending secrets into ACP or acpx harness sessions, and review prompts before routing them to a persistent session. <br>
Risk: Direct acpx flows can invoke local adapter commands and external coding harnesses from the current workspace. <br>
Mitigation: Confirm the intended harness, working directory, and command path before executing direct acpx shell commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zch-danny/openclaw-acp-router) <br>
- [Publisher profile](https://clawhub.ai/user/zch-danny) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON tool-call examples and shell command templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May route work into persistent ACP harness sessions and may propose local acpx installation, gateway restart, or ~/.acpx/config.json changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
