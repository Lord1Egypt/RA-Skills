## Description: <br>
Generates terminal recordings using VHS tape scripts and produces GIF outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to create terminal demo recordings for documentation, tutorials, and CLI workflow demonstrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tape files execute terminal commands and may perform unintended actions if they are untrusted or not reviewed. <br>
Mitigation: Review tape files before running them and execute only trusted recordings. <br>
Risk: Published recordings can expose secrets, private paths, credentials, or proprietary workflow details. <br>
Mitigation: Prefer local GIF output by default and use the publish option only after reviewing the recording content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scry-vhs-recording) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scry) <br>
- [VHS Execution Guide](modules/execution.md) <br>
- [VHS Tape Syntax Reference](modules/tape-syntax.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and tape code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local VHS tape validation and recording, with GIF output verification and optional public publishing guidance.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
