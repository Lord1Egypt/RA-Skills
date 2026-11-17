## Description:

Nerve Bridge controls Trae via macOS AppleScript and waits for completion confirmation through a local feedback mechanism.

This skill is ready for commercial/non-commercial use.

## Publisher:

[88901111hz-lang](https://clawhub.ai/user/88901111hz-lang)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill on macOS to send instructions to Trae, execute code or commands in that IDE, and wait for a completion signal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive Trae through macOS Accessibility and send IDE instructions that execute code or commands.

Mitigation: Install only when that automation is intentional, review instructions before sending them, and avoid use in sensitive repositories or active sessions.

Risk: The local completion file is a weak feedback signal and may be stale, spoofed, or cleaned up unsafely.

Mitigation: Treat feedback as unreliable unless the skill is changed to use per-run authenticated feedback and safer cleanup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/88901111hz-lang/skills/nerve-bridge-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python snippets; command output may include JSON feedback.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, python3, osascript, Trae, and Accessibility permissions for System Events and Terminal.]

## Skill Version(s):

v1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
