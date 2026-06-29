## Description: <br>
LYGO FractalWeaver analyzes self-similar or fractal images and maps their visual structure into evolving audio textures, stereo WAV output, and structured FractalWeave profile data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deepseekoracle](https://clawhub.ai/user/deepseekoracle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and agent operators use this skill to turn fractal or other self-similar images into evolving audio textures and profile JSON for creative workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes local audio and profile outputs, which can overwrite files if output paths are reused. <br>
Mitigation: Run it in a clean working folder and review output paths before execution. <br>
Risk: When a compatible local 3-Brain component is present, the skill may automatically add summaries to local memory. <br>
Mitigation: Use a clean folder, review local components, and do not place untrusted lyra_brain.py files beside the skill. <br>
Risk: Publisher token and publish commands appear in the artifact documentation but are not required for normal use. <br>
Mitigation: Ignore publishing and token-loading commands unless you maintain this ClawHub package. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/deepseekoracle/lygo-fractalweaver) <br>
- [LYGO RESONANCE companion site](https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files] <br>
**Output Format:** [Markdown guidance with bash commands; generated runs can produce WAV audio and JSON profile files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local execution may write WAV, JSON profile, generated fractal images, and optional memory nodes when compatible local components are present.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and fractalweaver.py __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
