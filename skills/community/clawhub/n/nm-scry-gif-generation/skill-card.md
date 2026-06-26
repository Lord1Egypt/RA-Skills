## Description: <br>
Converts webm/mp4 video files to optimized GIFs via ffmpeg with configurable quality settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to convert local video recordings into optimized GIFs for documentation, demos, and lightweight sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation triggers may cause the agent to suggest video conversion commands in unrelated contexts. <br>
Mitigation: Review suggested actions before running commands and proceed only when the task is an intended video-to-GIF conversion. <br>
Risk: Incorrect input or output paths could convert the wrong local file or write output to an unintended location. <br>
Mitigation: Confirm the source video path, destination path, and ffmpeg command options before execution. <br>
Risk: The workflow depends on a local ffmpeg installation. <br>
Mitigation: Install ffmpeg only through a trusted package manager and verify availability before conversion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-scry-gif-generation) <br>
- [Scry project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scry) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces ffmpeg command suggestions and verification steps; GIF files are generated locally when the user runs the commands.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
