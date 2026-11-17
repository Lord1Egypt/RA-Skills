## Description:

Control and automate Linux X11 desktop GUIs with screenshots, window inspection, clicking, typing, hotkeys, scrolling, and window management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gedigi](https://clawhub.ai/user/gedigi)

### License/Terms of Use:


## Use Case:

Developers, QA engineers, and agents use Peekaboox to automate GUI workflows on Linux X11 desktops by capturing screen state, locating targets visually, and issuing mouse, keyboard, scroll, and window-management commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad X11 desktop control can change real applications, trigger destructive controls, or close windows.

Mitigation: Use a dedicated test session or VM when possible and require explicit user approval before hotkeys, typing, clicks on destructive controls, or closing windows.

Risk: Screenshots can expose sensitive information visible on the desktop.

Mitigation: Avoid running the skill while sensitive apps or unsaved work are visible, and inspect captured screenshots before taking follow-up actions.

Risk: Clicking and screenshot behavior is not hardened for adversarial or shared-user environments.

Mitigation: Limit use to trusted sessions and harden the click and screenshot scripts before deployment in shared or adversarial environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gedigi/skills/peekaboox)
- [ClawHub Publisher Profile](https://clawhub.ai/user/gedigi)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline bash commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require an X11 session with DISPLAY set and xdotool, wmctrl, and scrot installed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
