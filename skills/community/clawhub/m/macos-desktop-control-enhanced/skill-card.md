## Description:

macOS Desktop Control Enhanced provides system-wide desktop automation on macOS, including screenshot capture, process management, clipboard operations, system information, application control, and direct mouse, keyboard, and screen interaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pry520okgpt](https://clawhub.ai/user/pry520okgpt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to control and query macOS desktops for testing, data collection, accessibility workflows, and local system automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture visible screen content and read or overwrite clipboard data.

Mitigation: Use it only in controlled macOS sessions with explicit user-directed commands, and review captured or clipboard data before sharing it.

Risk: The skill can type, click, focus applications, terminate processes, and otherwise affect the active desktop.

Mitigation: Validate coordinates, bundle identifiers, process identifiers, and text inputs before execution, especially when values come from web pages, files, clipboard contents, or model output.

Risk: The security verdict flags the release as suspicious because sensitive and destructive desktop actions lack sufficient scoping, safeguards, or input validation.

Mitigation: Review the skill before installing and restrict use to trusted workflows where a human can supervise desktop-control effects.

## Reference(s):

- [macOS Desktop Control Enhanced API Reference](references/api_reference.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with inline Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshot file paths, process metadata, clipboard text, system information, and desktop-control actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
