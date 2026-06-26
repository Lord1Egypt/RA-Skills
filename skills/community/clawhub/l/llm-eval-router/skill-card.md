## Description: <br>
Shadow-test local Ollama models against a cloud baseline with a multi-judge ensemble and automatically promote models when statistically proven equivalent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design a shadow evaluation pipeline that compares local Ollama models against cloud model baselines, scores results with a judge ensemble, and routes eligible tasks to lower-cost local models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evaluated prompts and outputs may be sent to Anthropic, OpenAI, or Google Gemini using the user's own provider accounts. <br>
Mitigation: Use the skill only for data that is acceptable under the chosen provider terms and retention settings, and keep API keys scoped and out of logs. <br>
Risk: Optional scheduled runs can create repeated provider calls and ongoing API spend. <br>
Mitigation: Enable cron, systemd, or launchd schedules deliberately and monitor provider usage, local logs, and evaluation cadence. <br>
Risk: Automatically promoted local models may be inappropriate for high-safety or highly confidential tasks. <br>
Mitigation: Keep high-safety tasks on cloud models with safety controls and review routing policies, score thresholds, and demotion behavior before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/llm-eval-router) <br>
- [Skill homepage](https://github.com/reddinft/skill-llm-eval-router) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and YAML examples plus operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local Ollama requirements, provider API key requirements, optional scheduling guidance, and evaluation thresholds.] <br>

## Skill Version(s): <br>
1.2.2 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
