## Description: <br>
Intelligent LLM proxy that routes requests to appropriate models based on complexity across Anthropic, OpenAI, Gemini, Kimi/Moonshot, and Ollama. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexrudloff](https://clawhub.ai/user/alexrudloff) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to install, configure, and operate an OpenAI-compatible LLM routing proxy that selects providers and models by request complexity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider API keys or OAuth tokens may be exposed through shared configuration files or repositories. <br>
Mitigation: Keep provider credentials out of shared files and repos, and restrict config.yaml permissions. <br>
Risk: Routing requests through paid providers can create unexpected usage or billing. <br>
Mitigation: Monitor provider billing and review model routing choices before sustained use. <br>
Risk: The local proxy or optional background service could be exposed or left running unintentionally. <br>
Mitigation: Keep the proxy bound to localhost unless intentional exposure is required, and enable the LaunchAgent only when continuous operation is desired. <br>


## Reference(s): <br>
- [LLM Router repository](https://github.com/alexrudloff/llmrouter) <br>
- [OpenClaw repository](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash, YAML, JSON, and XML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, local server operation, provider routing configuration, OpenClaw integration, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
