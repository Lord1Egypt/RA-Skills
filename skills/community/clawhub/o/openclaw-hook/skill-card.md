## Description: <br>
Create, debug, and maintain OpenClaw Gateway internal hooks for agent lifecycle events, including bootstrap context injection and Telegram notification troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cbd2020](https://clawhub.ai/user/cbd2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, register, debug, and test OpenClaw Gateway internal hooks that respond to agent bootstrap events, inject virtual files, inspect workspace state, or send notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or adapted hooks can persist in OpenClaw Gateway, read local OpenClaw configuration, inject bootstrap context, and send Telegram messages when enabled. <br>
Mitigation: Before enabling a hook, review the JavaScript, confirm which events it handles, which files it reads, what bootstrap context it injects, and where Telegram messages are sent; disable the hook when it is no longer needed. <br>


## Reference(s): <br>
- [OpenClaw Hook Development on ClawHub](https://clawhub.ai/cbd2020/openclaw-hook) <br>
- [Complete OpenClaw hook example](references/complete-example.js) <br>
- [Telegram test script](scripts/test-telegram.js) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JavaScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hook registration steps, debugging checks, Telegram test commands, and example handler code.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
