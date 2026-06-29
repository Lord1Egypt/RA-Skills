## Description: <br>
LYGO Ollama Army & Assistant Hub sets up a persistent local Ollama bot army for mundane tasking and lets users summon LYGO champions as specialized agent helpers for local automation and creative workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deepseekoracle](https://clawhub.ai/user/deepseekoracle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to configure and run local Ollama daemons, queue local tasks, summon documented LYGO champion personas, and prepare LYGO RESONANCE image-to-sound or profile workflows. It is intended for users who want a local-first assistant hub with human-reviewed queue and growth controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local daemons and queue processing can perform work on local files once task files are present. <br>
Mitigation: Use a dedicated working folder and manually review queue files before daemons process them. <br>
Risk: Self-growing mode can propose or launch additional roles based on recent task results. <br>
Mitigation: Keep --grow disabled until the launcher and daemon behavior have been reviewed and approved. <br>
Risk: Visible Windows console spawning and command-line options can change runtime behavior. <br>
Mitigation: Keep --visible-windows off by default and do not pass role, model, or champion values from untrusted sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deepseekoracle/lygo-ollama-army) <br>
- [LYGO RESONANCE companion site](https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html) <br>
- [Ollama](https://ollama.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration notes, and JSON queue-task examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local daemon setup steps, champion prompt guidance, task queue JSON, and recommendations for safe local operation.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
