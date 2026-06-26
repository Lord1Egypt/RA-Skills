## Description: <br>
Converts image sequences or grid sprite sheets into GIF animations with configurable FPS, looping, layout slicing, and optional size compression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guanyang](https://clawhub.ai/user/guanyang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate GIFs from ordered image frames or grid sprite sheets, including sticker-style GIFs that need FPS, loop, layout, and file-size controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local shell and Python code, creates a virtual environment, and installs Pillow. <br>
Mitigation: Review the scripts before use, install from trusted sources, and keep Pillow current or pinned to a reviewed version. <br>
Risk: The skill reads user-supplied image files, which carries ordinary file-processing risk for malformed or untrusted images. <br>
Mitigation: Use trusted input images where possible and run the skill in a constrained working directory containing only the files needed for the GIF. <br>
Risk: Optional size compression invokes the system gifsicle binary when max-size compression is requested. <br>
Mitigation: Install gifsicle from a trusted package source and verify it is available before relying on compression behavior. <br>


## Reference(s): <br>
- [Gif Maker on ClawHub](https://clawhub.ai/guanyang/gif-maker) <br>
- [guanyang publisher profile](https://clawhub.ai/user/guanyang) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated GIF files on disk] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports directory image sequences, single sprite sheets with layout, FPS, output path, and optional max-size compression settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
