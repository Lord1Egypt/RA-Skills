## Description: <br>
Use OverRec CLI to take screenshots, draw overlay rectangles, list monitors, find windows by title, or snap app windows to exact positions and sizes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metaphorproj](https://clawhub.ai/user/metaphorproj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support agents, and operators use this skill to capture or annotate screen regions and position Windows application windows during troubleshooting, documentation, and interactive workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots or repeated screen captures can save sensitive screen contents. <br>
Mitigation: Choose a specific capture region, set a duration or frame limit for monitoring, select the output folder deliberately, and delete saved frames that may contain private information. <br>
Risk: The skill depends on a local OverRec CLI executable for screen capture, overlays, and window placement. <br>
Mitigation: Use it only when the local OverRec installation is trusted and verify the command target before capturing the screen or moving windows. <br>


## Reference(s): <br>
- [OverRec Microsoft Store listing](https://apps.microsoft.com/detail/9pdn41kpj3hg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with command examples, file paths, and brief status notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save screenshot images or repeated capture frames to user-selected files; screenshots may be copied to the clipboard when OverRec defaults are used.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
