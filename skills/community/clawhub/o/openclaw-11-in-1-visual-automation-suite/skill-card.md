## Description:

Windows-only visual automation toolkit for screen capture, OCR, template matching, target localization, mouse clicks, keyboard input, temporary file cleanup, and looped desktop tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joriemancgemanne](https://clawhub.ai/user/joriemancgemanne)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to compose Windows desktop automation workflows that locate visual targets with OCR or image templates, then click, type, capture screenshots, clean temporary outputs, or repeat the workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture the full screen, which may expose private windows, secrets, passwords, or one-time codes visible on the desktop.

Mitigation: Use it only on controlled desktops, keep sensitive windows off screen, and avoid workflows involving passwords or one-time codes.

Risk: The skill can control the mouse and keyboard, so a wrong target match can trigger unintended desktop actions.

Mitigation: Run on bounded tasks, review target text and templates before use, and leave delays or checkpoints after clicks on slow interfaces.

Risk: Temporary OCR text and screenshots are written locally, and cleanup behavior can delete files from the selected temporary directory.

Mitigation: Use a dedicated temporary directory, review or patch cleanup behavior before valuable-file or production use, and clean temporary outputs after each run.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/joriemancgemanne/skills/openclaw-11-in-1-visual-automation-suite)
- [Publisher Profile](https://clawhub.ai/user/joriemancgemanne)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown instructions, Python call patterns, console status text, screenshots, OCR text files, and coordinate files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows 10/11 only; requires Python, OpenCV, pytesseract or another OCR engine, pyautogui, Pillow, and local template images for template matching.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
