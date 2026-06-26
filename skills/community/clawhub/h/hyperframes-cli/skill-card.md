## Description: <br>
HyperFrames CLI guides agents through the `npx hyperframes` dev loop for scaffolding, linting, visual inspection, preview, rendering, and environment troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas-kay8](https://clawhub.ai/user/lucas-kay8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run HyperFrames CLI commands for building and checking video projects, from project initialization through render and environment diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HyperFrames CLI commands can create files, copy or process media, download supporting tools or models, run local preview servers, and consume significant local resources. <br>
Mitigation: Review command paths, flags, and media inputs before execution, especially `init`, render commands, `--non-interactive`, and commands that download browsers or models. <br>


## Reference(s): <br>
- [HyperFrames CLI skill page](https://clawhub.ai/lucas-kay8/hyperframes-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advises Node.js >= 22, FFmpeg, and command review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
