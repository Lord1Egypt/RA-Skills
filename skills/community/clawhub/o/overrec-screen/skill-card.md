## Description:

OverRec Screen helps agents use OverRec CLI to capture screen regions, draw overlays, list monitors, find windows by title, and move or resize application windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metaphorproj](https://clawhub.ai/user/metaphorproj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate OverRec on Windows or WSL for screen capture, temporary visual highlighting, monitor inspection, and deterministic window placement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repeated screen captures can save sensitive screen content to disk.

Mitigation: Require an explicit capture region, interval, save location, and finite stop condition before watch-mode capture, and avoid sensitive screens.

Risk: Window-title searches can be unsafe if user-supplied text is pasted directly into shell commands.

Mitigation: Handle window titles as literal quoted arguments and avoid constructing shell commands from untrusted text.

## Reference(s):

- [OverRec Microsoft Store listing](https://apps.microsoft.com/detail/9pdn41kpj3hg)
- [OverRec Screen ClawHub skill page](https://clawhub.ai/metaphorproj/skills/overrec-screen)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct local screenshots to files or clipboard when the user requests capture.]

## Skill Version(s):

0.2.0 (source: artifact metadata and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
