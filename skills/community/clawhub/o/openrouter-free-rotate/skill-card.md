## Description: <br>
Scans OpenRouter for zero-cost models, benchmarks and scores them by capability, and can update OpenClaw model configuration with selected free models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liligit1815](https://clawhub.ai/user/liligit1815) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to rotate OpenClaw's OpenRouter free-model configuration after scanning, testing, and ranking available zero-cost models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite OpenClaw model configuration and optionally restart the gateway. <br>
Mitigation: Run --scan or --no-update first, back up ~/.openclaw/openclaw.json and ~/.openclaw/agents/main/agent/models.json, and only use --restart with monitoring and rollback in place. <br>
Risk: Passing an OpenRouter API key on the command line can expose it through shell history or process listings. <br>
Mitigation: Prefer the OPENROUTER_API_KEY environment variable over --api-key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liligit1815/openrouter-free-rotate) <br>
- [OpenRouter API endpoint used by the skill](https://openrouter.ai/api/v1) <br>
- [OpenClaw site referenced by API requests](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, json] <br>
**Output Format:** [Markdown guidance with shell command examples, terminal status output, configuration file updates, and optional JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenRouter API key and can write OpenClaw configuration files when update mode is enabled.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
