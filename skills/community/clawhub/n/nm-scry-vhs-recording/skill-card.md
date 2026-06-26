## Description: <br>
Generates terminal recordings using VHS tape scripts and produces GIF outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to validate VHS tape files, run terminal recording workflows, and produce GIF outputs for documentation and CLI tutorials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VHS tape files can execute local shell commands during recording. <br>
Mitigation: Read each tape like a shell script before running VHS, and verify output paths before recording. <br>
Risk: Published recordings can expose sensitive terminal content. <br>
Mitigation: Avoid `--publish` unless the recording is sanitized and safe to share publicly. <br>


## Reference(s): <br>
- [VHS Execution Guide](modules/execution.md) <br>
- [VHS Tape Syntax Reference](modules/tape-syntax.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/nm-scry-vhs-recording) <br>
- [Clawdis Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scry) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and VHS tape snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs recording workflow guidance for local VHS execution; generated recordings may create GIF, MP4, WebM, or screenshot files depending on the tape.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
