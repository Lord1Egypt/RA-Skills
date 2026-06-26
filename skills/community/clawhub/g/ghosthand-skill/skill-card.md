## Description: <br>
Use this skill when operating Ghosthand, a local Android control runtime exposed over a loopback HTTP API for OpenClaw or another agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[folklore25](https://clawhub.ai/user/folklore25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent operators use this skill to inspect Android UI state and perform bounded Ghosthand actions such as capability checks, selector-based clicks, text entry, scrolling, screenshots, wait conditions, clipboard transfer, notifications, and route debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ghosthand can drive sensitive Android control capabilities through a local runtime. <br>
Mitigation: Install only when the separate Ghosthand Android runtime is trusted, keep Ghosthand permissions and policy narrow, and require explicit confirmation before purchases, account changes, message sending, deletions, or public posting. <br>
Risk: Android screen, clipboard, screenshot, and notification use can expose unrelated sensitive content during operation. <br>
Mitigation: Avoid running Ghosthand while unrelated sensitive content is visible or copied, and use capability checks before sensitive routes. <br>


## Reference(s): <br>
- [Ghosthand API Quick Reference](resources/references/ghosthand-api-quick-reference.md) <br>
- [Ghosthand-Skill on ClawHub](https://clawhub.ai/folklore25/ghosthand-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown] <br>
**Output Format:** [Markdown with HTTP route examples and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing instructions for a local Android control runtime; it does not include executable code.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
