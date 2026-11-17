## Description:

Controls local and network printers on Windows to list printers, print files or text, check status, and set the default printer with partial name matching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangpl666ya](https://clawhub.ai/user/zhangpl666ya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent inspect Windows printer availability, send approved print jobs, check printer health, and change the default printer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PowerShell fallbacks may treat printer names or file paths as executable script content.

Mitigation: Prefer pywin32 and use only trusted printer names and file paths until the fallback passes those values as data.

Risk: Printing can consume paper, ink, toner, or expose content at the wrong physical printer.

Mitigation: Require explicit confirmation of the printer, content, and copy count before each print operation.

Risk: Changing the default printer persists after the command completes.

Mitigation: Confirm the intended default printer before changing it and restore the prior default when the change was temporary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangpl666ya/skills/printer-control)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text console output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows printer operations can consume physical resources, disclose printed content, or persistently change the default printer.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
