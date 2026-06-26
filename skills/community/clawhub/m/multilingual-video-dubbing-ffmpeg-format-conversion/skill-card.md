## Description: <br>
Convert media files between formats - video containers, audio formats, and codec transcoding <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, media engineers, and automation agents use this skill to choose FFmpeg commands for container conversion, codec transcoding, audio format conversion, quality tuning, and batch media conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FFmpeg commands can overwrite existing media files when output names collide. <br>
Mitigation: Check output filenames before running commands and run examples only in directories containing files intended for conversion. <br>
Risk: Batch conversion examples can affect many files in the current directory. <br>
Mitigation: Review shell globs and run batch examples in a controlled working directory before applying them to valuable media. <br>
Risk: Using an untrusted FFmpeg binary can introduce security risk. <br>
Mitigation: Install FFmpeg only from a trusted source. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces FFmpeg command examples and concise conversion guidance; it does not execute commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
