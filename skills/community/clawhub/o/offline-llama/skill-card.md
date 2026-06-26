## Description: <br>
Manages local Ollama models with health monitoring, fallback, self-healing, and offline-first operation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[and-ray-m](https://clawhub.ai/user/and-ray-m) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to keep local Ollama-backed workflows available by checking model health, switching models, and recovering from service or resource problems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over local Ollama services and model storage, including restarts, cleanup, model switching, and reinstallations. <br>
Mitigation: Require explicit confirmation before restarts, cleanup, model changes, or reinstallations, and review proposed commands before execution. <br>
Risk: Remote-model fallback may send prompts or data outside the local environment despite the local-first privacy posture. <br>
Mitigation: Disable remote fallback unless it is explicitly approved, configured, and reviewed for the data being processed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/and-ray-m/offline-llama) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with command names and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Ollama service restarts, cache cleanup, model switching, model reinstallations, and remote fallback depending on agent permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
