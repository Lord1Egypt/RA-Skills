## Description: <br>
IdleClaw helps agents share idle Ollama inference capacity with a community network or use community inference when API credits run out. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[futurejunk](https://clawhub.ai/user/futurejunk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use IdleClaw to contribute local Ollama model capacity to a shared inference network, consume streamed community inference, and check available network models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Consume mode sends prompts through community inference infrastructure, which can expose sensitive or regulated text to the routing path. <br>
Mitigation: Do not send secrets, credentials, proprietary code, regulated data, or personal information through consume mode. <br>
Risk: Contribute mode shares local Ollama capacity with the community and can consume CPU, GPU, and memory while running. <br>
Mitigation: Use a trusted or self-hosted IDLECLAW_SERVER when possible, monitor local resource use, and stop the script when you no longer want to share capacity. <br>


## Reference(s): <br>
- [IdleClaw on ClawHub](https://clawhub.ai/futurejunk/idleclaw) <br>
- [futurejunk publisher profile](https://clawhub.ai/user/futurejunk) <br>
- [IdleClaw security assessment](https://github.com/futurejunk/idleclaw/blob/main/security/SECURITY.md) <br>
- [Ollama download](https://ollama.com/download) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and streamed text responses from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and ollama. Uses IDLECLAW_SERVER for the routing server and OLLAMA_HOST for the local Ollama endpoint.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
