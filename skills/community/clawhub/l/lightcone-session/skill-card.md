## Description: <br>
Manual step-by-step computer control via Lightcone sessions for fine-grained browser or desktop automation, multi-step workflows, login sequences, precise click-by-click interaction, screenshots, and cloud computer actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddieogola](https://clawhub.ai/user/eddieogola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manually control a remote cloud browser or desktop through Lightcone sessions for multi-step website and application workflows. It supports navigation, clicks, typing, hotkeys, screenshots, HTML extraction, debug commands, and session cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote cloud computer sessions may expose account pages or sensitive site content during login, screenshots, or HTML extraction. <br>
Mitigation: Use the skill only with accounts and sites you are comfortable exposing to a remote cloud computer, avoid real passwords or sensitive data unless explicitly intended, and approve private page extraction case by case. <br>
Risk: Debug actions can run shell commands in the cloud computer. <br>
Mitigation: Review each debug command before execution, avoid untrusted commands, and close sessions when work is complete. <br>


## Reference(s): <br>
- [Lightcone documentation](https://docs.lightcone.ai) <br>
- [ClawHub skill page](https://clawhub.ai/eddieogola/lightcone-session) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Text, Configuration] <br>
**Output Format:** [Markdown with structured tool-call examples and action parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TZAFON_API_KEY; actions can return screenshots, page HTML, command output, and session identifiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
