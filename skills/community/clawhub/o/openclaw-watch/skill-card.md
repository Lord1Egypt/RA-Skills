## Description: <br>
OpenClaw Watch provides local security scanning, PII sanitization, and intent-action mismatch checks for agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NeuZhou](https://clawhub.ai/user/NeuZhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to scan installed skills and workspaces, sanitize secret-containing text before external use, check suspicious messages, and compare intended actions with proposed commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence flags that the skill directs agents to run an npm package resolved as @latest. <br>
Mitigation: Pin a reviewed OpenClaw Watch package version before routine use and require approval before updating it. <br>
Risk: The release evidence advises caution around automatic periodic scans, broad local paths, and secret-containing text. <br>
Mitigation: Keep scans scoped to intended directories, disable automatic periodic scans when not needed, and require explicit approval before sanitizing sensitive text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NeuZhou/openclaw-watch) <br>
- [Project homepage](https://github.com/NeuZhou/openclaw-watch) <br>
- [Issue tracker](https://github.com/NeuZhou/openclaw-watch/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and scanner result summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and invokes the OpenClaw Watch npm package from shell commands.] <br>

## Skill Version(s): <br>
6.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
