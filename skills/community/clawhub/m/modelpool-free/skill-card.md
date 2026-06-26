## Description: <br>
ModelPool (Free) helps OpenClaw users discover free OpenRouter models, configure multi-key rotation and fallback chains, and run repair diagnostics for model connectivity and configuration issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meilihulee](https://clawhub.ai/user/meilihulee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up and maintain free OpenRouter-backed model providers for OpenClaw, including model discovery, key rotation, fallback configuration, and repair workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenRouter API keys may be stored locally in plaintext under ~/.openclaw and in OpenClaw configuration or backup files. <br>
Mitigation: Use revocable keys, limit their scope where possible, rotate keys after testing, and protect local OpenClaw configuration and backup files. <br>
Risk: Repair and setup workflows can rewrite OpenClaw configuration, clean sessions or logs, test endpoints, and restart OpenClaw. <br>
Mitigation: Run these commands only when those operational changes are acceptable, and review or back up the OpenClaw configuration before applying repairs. <br>
Risk: Provider endpoint checks use configured base URLs and keys. <br>
Mitigation: Review provider base URLs and the artifact identity before running setup or repair commands. <br>


## Reference(s): <br>
- [OpenRouter](https://openrouter.ai) <br>
- [OpenRouter Keys](https://openrouter.ai/keys) <br>
- [OpenRouter Models API](https://openrouter.ai/api/v1/models) <br>
- [OpenRouter Registration and API Key Guide](docs/openrouter-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify local OpenClaw configuration and key storage files when its commands are executed.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and setup.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
