## Description:

Control this macOS desktop via screenshots, AppleScript, mouse/keyboard automation, OCR/template matching, and verify loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igallta](https://clawhub.ai/user/igallta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to automate real macOS desktop workflows when direct APIs, shell commands, or browser automation are not enough. It supports screenshot-guided interaction, AppleScript window/app control, mouse and keyboard automation, OCR/template targeting, and verify-after-action loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can receive broad Screen Recording, Accessibility, or Automation permissions that allow screen observation and input control.

Mitigation: Grant permissions only in trusted contexts, use the skill only for tasks the user explicitly wants automated, and stop before public submissions or destructive actions unless specifically authorized.

Risk: Unsafe AppleScript input handling can make untrusted app names or key-combo strings risky.

Mitigation: Avoid feeding untrusted app names or key-combo strings to the helper and review commands before execution.

Risk: The documented unpinned pip command can install different dependency versions over time.

Mitigation: Prefer a pinned virtual environment for repeatable installation.

## Reference(s):

- [Source Notes](references/source-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON helper outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper emits JSON for screenshot capture, app/window state, mouse and keyboard actions, and template matching.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
