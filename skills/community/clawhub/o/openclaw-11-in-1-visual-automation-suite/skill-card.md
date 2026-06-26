## Description: <br>
Windows-only visual automation toolkit for screen capture, OCR, template matching, mouse and keyboard control, environment setup, cleanup, and repeatable task loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joriemancgemanne](https://clawhub.ai/user/joriemancgemanne) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate Windows desktop workflows that need visual target detection, OCR text extraction, template-based localization, input simulation, and repeated task execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full-screen screenshots and OCR can capture passwords, private documents, or other sensitive on-screen content. <br>
Mitigation: Run the skill only when sensitive content is not visible, and delete temporary screenshot and OCR files after use. <br>
Risk: Mouse and keyboard automation can perform unintended actions if target localization is wrong or the active window changes. <br>
Mitigation: Review target coordinates or recognition results before input control, and prefer workflows that require explicit confirmation before clicks or typing. <br>
Risk: Temporary screenshots, OCR results, and coordinate files may retain sensitive data if cleanup is skipped or interrupted. <br>
Mitigation: Run the cleanup step after each workflow and verify the temporary directory is cleared before ending the session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joriemancgemanne/openclaw-11-in-1-visual-automation-suite) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with Python automation functions and call-style commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows 10/11 only; uses full-screen screenshots, OCR results, template images, mouse control, keyboard input, and temporary files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
