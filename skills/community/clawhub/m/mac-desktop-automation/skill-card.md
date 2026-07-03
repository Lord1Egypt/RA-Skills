## Description: <br>
Advanced desktop automation with mouse, keyboard, screen capture, window management, clipboard operations, and natural-language task execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyafeichina](https://clawhub.ai/user/liyafeichina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to let an agent control a local desktop through mouse, keyboard, screenshot, clipboard, window, and application-launch operations. It is suited for desktop workflow automation where the operator intentionally grants live-desktop control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a live desktop through mouse, keyboard, clipboard, screenshots, and application launch actions. <br>
Mitigation: Install only when that level of control is intended; keep failsafe and approval mode enabled and test first in a non-sensitive environment. <br>
Risk: Screenshots and clipboard contents may expose passwords, private documents, or other sensitive data. <br>
Mitigation: Avoid exposing sensitive windows while the skill is active and treat screenshots, clipboard data, and logs as sensitive local artifacts. <br>
Risk: Weak default guardrails could allow unintended actions if an agent misinterprets a task or the screen state. <br>
Mitigation: Review planned actions, require confirmation for high-impact operations, and stop execution immediately with the configured failsafe if behavior diverges. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liyafeichina/mac-desktop-automation) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [AI agent guide](artifact/AI_AGENT_GUIDE.md) <br>
- [Quick reference](artifact/QUICK_REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions, Files] <br>
**Output Format:** [Markdown guidance with Python snippets and shell commands; runtime helpers may create screenshots or update clipboard and desktop state.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Desktop actions depend on local OS permissions, visible screen state, installed applications, and enabled safety settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
