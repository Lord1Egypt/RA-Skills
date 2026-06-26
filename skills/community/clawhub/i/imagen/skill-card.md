## Description: <br>
Genera imagenes con calidad cheap, medium, good o top usando OpenRouter y la configuracion activa de OpenClaw, y guarda los archivos en el workspace actual del agente. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Perilla](https://clawhub.ai/user/Perilla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to route image-generation requests through OpenRouter with selected quality, size, and aspect-ratio settings. The generated image is saved in the current agent workspace for follow-up use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts are sent to OpenRouter. <br>
Mitigation: Avoid including secrets, private documents, or sensitive business data in prompts. <br>
Risk: The skill may read local OpenClaw auth-profile files when OPENROUTER_API_KEY is not set. <br>
Mitigation: Set OPENROUTER_API_KEY explicitly for tighter credential control. <br>
Risk: Generated images remain in the agent workspace. <br>
Mitigation: Review workspace retention practices and remove generated files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Imagen release page](https://clawhub.ai/Perilla/imagen) <br>


## Skill Output: <br>
**Output Type(s):** [Files, API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Generated image file plus JSON and text status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports quality levels cheap, medium, good, and top; optional image size 1K, 2K, or 4K; and supported aspect ratios including 1:1, 16:9, 9:16, and 21:9.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
