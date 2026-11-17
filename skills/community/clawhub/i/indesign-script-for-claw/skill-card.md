## Description:

Generates Adobe InDesign automation scripts for general layout tasks and manga typesetting workflows, with Windows and macOS support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jqk4388](https://clawhub.ai/user/jqk4388)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, manga localization teams, and developers use this skill to generate or run Adobe InDesign scripts for batch layout changes, image placement, LabelPlus text import, style application, and manga lettering automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trusted-looking configuration files can trigger local script or helper execution through the manga layout launcher or segmentation helper path.

Mitigation: Install only from a trusted source, review companion run_manga_layout.sh or run_manga_layout.ps1 files, and inspect any segmentation.pythonScriptPath value before running.

Risk: InDesign automation can modify layout documents and project files during execution.

Mitigation: Back up InDesign documents before running automation and disable segmentation when the external helper is not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jqk4388/skills/indesign-script-for-claw)
- [Project homepage](https://github.com/jqk4388/Mangahanhua-Scripts-for-Indesign/tree/master/Indesign-script-for-claw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSX, shell, PowerShell, Python command snippets, and JSON configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Adobe InDesign plus local Python and PowerShell or shell launchers on Windows or macOS.]

## Skill Version(s):

1.1.51 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
