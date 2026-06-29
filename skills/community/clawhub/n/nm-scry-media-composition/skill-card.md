## Description: <br>
Combines GIFs and videos into composite tutorials with vertical or grid layouts via ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical content authors use this skill to combine terminal, browser, image, GIF, and video outputs into tutorial or documentation media using manifest-defined ffmpeg layouts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate broadly on media or composition wording. <br>
Mitigation: Review and narrow trigger wording before installation if activation should be limited to explicit ffmpeg or media-composition requests. <br>
Risk: Generated ffmpeg shell commands can read local media files or overwrite output paths. <br>
Mitigation: Inspect commands, input paths, and output destinations before execution, and run them only in the intended working directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scry-media-composition) <br>
- [Night Market Scry plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scry) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML manifest examples and bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces ffmpeg composition instructions; generated commands may read media inputs and overwrite declared output files.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
