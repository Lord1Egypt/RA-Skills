## Description: <br>
Converts webm/mp4 video files to optimized GIFs via ffmpeg with configurable quality settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn local webm, mp4, mov, or avi recordings into shareable GIFs with ffmpeg. It helps select quality, frame rate, scale, palette, and dithering settings and verify the generated output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic prompts mentioning video, GIFs, optimization, or ffmpeg may activate the skill. <br>
Mitigation: Confirm the source video path, output GIF path, and selected conversion settings before allowing any ffmpeg command to run. <br>
Risk: ffmpeg conversion commands process local files and can overwrite or create outputs at user-provided paths. <br>
Mitigation: Validate that the input file exists, review the output filename, and verify the generated GIF before relying on the result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scry-gif-generation) <br>
- [OpenClaw homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/scry) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local ffmpeg command suggestions, validation steps, troubleshooting guidance, and output verification instructions.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter states 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
