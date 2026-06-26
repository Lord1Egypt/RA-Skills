## Description: <br>
Convert a local video into an iPhone-compatible Live Photo package (.pvt) for Apple Photos, lock-screen wallpaper use, or Live Photo sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hekaiii](https://clawhub.ai/user/hekaiii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and other external users use this skill to convert short local videos into Apple Photos-importable Live Photo packages for iPhone wallpaper or sharing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may install or use local media tools such as ffmpeg, makelive, and pipx. <br>
Mitigation: Review and approve dependency installation commands before running the skill. <br>
Risk: Generated output files or a .pvt directory with the same base name may be overwritten or removed. <br>
Mitigation: Run conversions in a dedicated output folder and choose a fresh base output path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hekaiii/live-photo-maker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with shell commands and generated local media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce an optimized MP4, cover JPG, .pvt Live Photo package, and ZIP archive when run with local media tools.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
