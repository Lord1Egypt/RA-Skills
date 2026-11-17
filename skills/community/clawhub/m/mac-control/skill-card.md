## Description:

Control Mac via mouse/keyboard automation using cliclick and AppleScript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easonc13](https://clawhub.ai/user/easonc13)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to automate macOS UI workflows, including taking screenshots, inspecting window bounds, calibrating coordinate scaling, and issuing mouse or keyboard actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can issue real mouse and keyboard actions in the active macOS UI.

Mitigation: Use the skill only for tightly scoped, user-directed automation and verify coordinates or screenshots before important clicks.

Risk: Screenshots under /tmp and calibration files under ~/.clawdbot may expose sensitive screen contents or environment details.

Mitigation: Treat generated files as sensitive, avoid use while private data is visible, and delete temporary captures when they are no longer needed.

Risk: The security scan reports an AppleScript injection flaw.

Mitigation: Avoid passing untrusted application names into scripts and review or harden the package before using it on private, financial, administrative, or security-sensitive accounts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/easonc13/skills/mac-control)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May refer to generated screenshot files, calibration JSON, and coordinate values during agent-guided macOS UI automation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
