## Description:

Export specific pages from PPT, PPTX, or ODP files to cropped PDF via ppt2fig.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elliottzheng](https://clawhub.ai/user/elliottzheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document authors use this skill to export selected presentation slides into cropped, paper-ready PDF figures and to choose an available LibreOffice, WPS, or PowerPoint backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or run an unpinned Windows executable.

Mitigation: Use a trusted local ppt2fig installation or a version-pinned binary with checksum verification before running exports.

Risk: Executable lookup can select a dist/ppt2fig-cli.exe file from a shared or untrusted workspace.

Mitigation: Run the skill from trusted workspaces only and verify the selected executable path before execution.

Risk: The release security verdict is suspicious despite no individual risk findings being listed.

Mitigation: Review the skill before installing, especially on Windows, and install only if the ppt2fig GitHub release source is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elliottzheng/skills/ppt2fig-export)
- [ppt2fig project homepage](https://github.com/elliottzheng/ppt2fig)
- [ppt2fig CLI Windows release download](https://github.com/elliottzheng/ppt2fig/releases/latest/download/ppt2fig-cli.exe)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for generating PDF outputs from presentation inputs; output path depends on the selected file, page range, backend, and crop options.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
