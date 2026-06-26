## Description: <br>
Route tasks to the optimal cloud or local model based on task characteristics: coding, analysis, reasoning, creative, or general. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tooled-app](https://clawhub.ai/user/tooled-app) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to classify prompts and choose a suitable Ollama model before or during task execution. It helps balance quality, latency, local privacy preference, and availability across configured local and cloud model options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routing may select cloud models for prompts that contain confidential code, personal data, credentials, or proprietary material. <br>
Mitigation: Prefer local mode for sensitive tasks and review routing preferences before sending prompt content to a cloud-hosted model. <br>
Risk: The helper prints the task text to the terminal, which may expose sensitive prompt content in shell history, logs, or shared screens. <br>
Mitigation: Avoid passing secrets or private content as task text, and run the helper only in terminals where command output is appropriately protected. <br>
Risk: Model recommendations depend on keyword classification and the configured registry, so a poor registry or ambiguous prompt can choose a less suitable model. <br>
Mitigation: Review the recommended model and reason before execution, and maintain the registry to reflect available models and current task preferences. <br>


## Reference(s): <br>
- [Ollama](https://ollama.com) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [ClawHub skill page](https://clawhub.ai/tooled-app/ollama-model-router) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; router.sh emits terminal text plus a JSON model recommendation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq, a model registry JSON file, and Ollama availability checks for local models.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
