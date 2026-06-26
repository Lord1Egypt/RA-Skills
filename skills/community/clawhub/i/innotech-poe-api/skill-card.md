## Description: <br>
Intelligent AI model selection and orchestration via Poe API for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nwcalvin](https://clawhub.ai/user/nwcalvin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to route programming, design, analysis, web search, image, video, and audio requests to Poe-hosted AI models with task-based model selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, code, datasets, and search queries are sent to Poe and selected model providers by design. <br>
Mitigation: Redact secrets and sensitive personal or proprietary data before use, and confirm the selected provider is acceptable for the workload. <br>
Risk: The skill requires a Poe API key for authentication. <br>
Mitigation: Store the key only in the POE_API_KEY environment variable and avoid hardcoding credentials in files or prompts. <br>
Risk: External model calls can consume quota or incur billing. <br>
Mitigation: Monitor quota and billing, and use the built-in max_calls_per_task control for bounded runs. <br>
Risk: The OpenAI dependency is declared broadly as openai>=1.0.0. <br>
Mitigation: Pin and review dependency versions in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nwcalvin/innotech-poe-api) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [MODEL_SELECTION_GUIDE.md](MODEL_SELECTION_GUIDE.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Python return values, dictionaries, strings, Markdown guidance, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POE_API_KEY and sends prompts to Poe-hosted models.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata, artifact/skill.json, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
