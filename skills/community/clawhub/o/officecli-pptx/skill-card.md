## Description:

Guides agents in creating, reading, editing, validating, and delivering PowerPoint .pptx presentations with OfficeCLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iceyliu](https://clawhub.ai/user/iceyliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when a task involves PPTX input or output, including creating slide decks, reading or extracting slide content, editing presentations, working with templates, and validating slide quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes pipe-to-shell and PowerShell iex installer commands for OfficeCLI.

Mitigation: Install only after trusting the installer source; prefer a pinned OfficeCLI release and verify its integrity before execution.

Risk: The skill may activate on broad presentation-related words and can guide edits to PPTX files.

Mitigation: Confirm the intended PPTX files and requested operation before allowing setup, reads, edits, or delivery actions.

## Reference(s):

- [OfficeCLI Releases](https://github.com/iOfficeAI/OfficeCLI/releases)
- [ClawHub Skill Page](https://clawhub.ai/iceyliu/skills/officecli-pptx)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated or modified PPTX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OfficeCLI for PPTX inspection, editing, validation, and rendering checks.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
