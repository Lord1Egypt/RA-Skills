## Description: <br>
Manage local LLM services such as Ollama, vLLM, and OpenAI-compatible API endpoints through a unified command interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to check local LLM service status, start Ollama on Windows, pull Ollama models, and send prompts through Ollama or configured OpenAI-compatible API endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and any configured API key may be sent to an OpenAI-compatible endpoint selected by the user environment. <br>
Mitigation: Use API mode only with trusted endpoints and avoid sending sensitive prompts unless the endpoint is approved for that data. <br>
Risk: The start and pull commands can launch a local service or download large model files. <br>
Mitigation: Run service start and model pull commands deliberately, and monitor local compute, storage, and network use. <br>
Risk: The skill may require sensitive credentials for configured API services. <br>
Mitigation: Store API keys in environment variables, restrict their scope, and avoid exposing command output or logs that may reveal credentials. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/534422530/llm-service-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text status messages, model lists, command results, or generated model responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use OPENAI_BASE_URL, OPENAI_API_KEY, and OPENAI_MODEL environment variables; prompts and credentials are sent to the configured endpoint when API mode is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
