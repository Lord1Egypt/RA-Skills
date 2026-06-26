## Description: <br>
Runs a local Ollama Moondream model to describe images supplied through chat or local file paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to route local image files to Moondream through Ollama and return concise natural-language image descriptions for downstream chat workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ollama service exposure beyond localhost could allow unintended access to local model endpoints. <br>
Mitigation: Install Ollama from official sources and keep it bound to localhost. <br>
Risk: Image paths may disclose or process local files the user did not intend to analyze. <br>
Mitigation: Only submit image paths that are intended for analysis. <br>
Risk: Model-generated image descriptions can be incorrect or unsafe to pass directly into another agent. <br>
Mitigation: Treat descriptions as untrusted model output and review them before downstream use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openclawzhangchong/moondream-vision-zc) <br>
- [Publisher profile](https://clawhub.ai/user/openclawzhangchong) <br>
- [Ollama download](https://ollama.com/download) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Natural-language text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated descriptions should be treated as untrusted model output before reuse by another model or agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
