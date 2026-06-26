## Description: <br>
Automates clicks on browser extension icons such as OpenClaw Browser Relay using system-level GUI automation for toolbar, extension icon, and system menu interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BinbinHihi](https://clawhub.ai/user/BinbinHihi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent run a Python GUI automation script that locates or clicks browser extension icons. It supports dry-run, screenshot, calibration, delay, browser, and coordinate options for desktop browser workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Desktop-level screen capture and mouse-click authority can interact with the wrong visible UI. <br>
Mitigation: Use dry-run first, keep the intended browser window focused, and confirm coordinates or calibration before running a real click. <br>
Risk: Screenshots can capture sensitive content from the visible desktop. <br>
Mitigation: Close sensitive windows before screenshot use and delete generated screenshot files after review. <br>
Risk: Automated clicks on login pages, wallet prompts, permission dialogs, or unknown coordinates can trigger unintended actions. <br>
Mitigation: Avoid using the skill on sensitive prompts or unknown coordinates, and restrict use to expected browser extension UI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BinbinHihi/openclaw-browser-extension-clicker) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash command examples; the script emits terminal text and can optionally save PNG screenshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May move and click the desktop mouse and may save screenshot files when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
