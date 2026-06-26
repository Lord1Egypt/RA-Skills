## Description: <br>
Combines GIFs and videos into composite tutorials with vertical or grid layouts via ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical content authors use this skill to combine local GIFs, videos, and images into tutorial-style composites. It guides manifest review, input validation, ffmpeg command execution, and output checks for vertical, horizontal, sequential, grid, overlay, and picture-in-picture layouts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad media-composition triggers may invoke the skill outside a narrowly intended task. <br>
Mitigation: Use the skill deliberately for media-composition work and confirm the requested output before running ffmpeg commands. <br>
Risk: Untrusted manifests may cause unexpected inputs, commands, or output paths to be used. <br>
Mitigation: Review manifests from untrusted sources before command execution and confirm ffmpeg outputs and temporary files are written to expected locations. <br>


## Reference(s): <br>
- [Claude Night Market scry plugin](https://github.com/athola/claude-night-market/tree/master/plugins/scry) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces ffmpeg composition guidance and validation steps for local media files.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
