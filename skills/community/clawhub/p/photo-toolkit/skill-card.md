## Description: <br>
Photography utility toolkit that converts RAW/JPG/HEIC photos to JPG thumbnails, finds photos by shooting date, generates layout previews, deflickers timelapse frames, and assembles video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[konanok](https://clawhub.ai/user/konanok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to process local camera photo sets: convert images, locate files by EXIF shooting date, build before/after layouts, deflicker timelapses, and assemble JPG frames into MP4 video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local photo folders and writes processed outputs, so incorrect paths or batch options can expose or modify local photo collections. <br>
Mitigation: Review configured paths, prefer dry-run or preview options where available, and keep backups before batch conversion or deflicker operations. <br>
Risk: The dependency helper can install system and Python packages if approved. <br>
Mitigation: Review dependency-install prompts before approving them and prefer installing Python packages inside a virtual environment. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/konanok/photo-skills) <br>
- [ClawHub skill page](https://clawhub.ai/konanok/photo-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON reports, JPG image outputs, and MP4 video outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local file processing; outputs depend on selected input paths, configuration, and script options.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, VERSION, changelog released 2026-05-20, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
