## Description:

Converts PPT/PPTX presentations into MP4 videos with background music, automatic slide duration, page transitions, and optional typewriter-style text reveal effects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoyiyong985](https://clawhub.ai/user/haoyiyong985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to guide conversion of presentation decks into MP4 videos with background audio, transition effects, and timing controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unreviewed hard-coded local converter script path.

Mitigation: Use only a trusted converter script path, prefer a packaged or relative verified script path, and review the script before execution.

Risk: The skill may install Python packages and use host applications during conversion.

Mitigation: Confirm dependencies and package sources before installation, pin dependencies where practical, and run in an environment appropriate for document conversion.

Risk: The skill may make a persistent Windows registry change for PowerPoint export quality.

Mitigation: Ask before changing system settings and document or revert registry changes when they are not required.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/haoyiyong985/ppt-to-video)
- [ClawHub skill page](https://clawhub.ai/haoyiyong985/skills/ppt-to-video)
- [LibreOffice](https://www.libreoffice.org/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides creation of MP4 video outputs through a local converter workflow.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
