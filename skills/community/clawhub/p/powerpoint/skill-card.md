## Description: <br>
Control PowerPoint app sessions, slides, notes, export, and presentation state with osascript workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers on macOS use this skill to control live Microsoft PowerPoint sessions through osascript when presentation state, notes, slideshow mode, or PowerPoint-rendered export must be preserved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automation may affect the wrong live presentation or slide if the active PowerPoint state is ambiguous. <br>
Mitigation: Confirm the exact deck, slide, view, and slideshow state before edits, then read the final state back after each change. <br>
Risk: Slide deletion, bulk reordering, note replacement, overwrite exports, or close-without-save can remove or disrupt user work. <br>
Mitigation: Require explicit confirmation for destructive actions and prefer copies, Save As paths, or one-slide tests before broad changes. <br>
Risk: Local memory files may accidentally retain sensitive presentation content if used carelessly. <br>
Mitigation: Keep ~/powerpoint notes limited to non-sensitive environment facts, paths, preferences, and reusable troubleshooting notes. <br>
Risk: Attaching to an existing user-owned PowerPoint session can interrupt unrelated decks or presenter flow. <br>
Mitigation: Do not close unrelated decks or quit PowerPoint after attaching unless the user explicitly approves that action. <br>


## Reference(s): <br>
- [ClawHub PowerPoint skill page](https://clawhub.ai/ivangdavila/powerpoint) <br>
- [PowerPoint skill homepage](https://clawic.com/skills/powerpoint) <br>
- [Execution Matrix](execution-matrix.md) <br>
- [Live Control Patterns](live-control-patterns.md) <br>
- [Safety Checklist](safety-checklist.md) <br>
- [Troubleshooting](troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with bash and AppleScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local ~/powerpoint notes and PowerPoint exports when the user requests those actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
