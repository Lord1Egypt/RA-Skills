## Description: <br>
Use AIsa for model routing, provider setup, and Chinese LLM access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure AIsa-backed model routing, inspect available model options, and prepare workflows for Chinese LLM access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses AISA_API_KEY and can send prompts, image URLs, and usage data to AIsa. <br>
Mitigation: Use a scoped or revocable API key when available, avoid sending sensitive content unless AIsa's data handling terms are acceptable, and rotate keys if exposure is suspected. <br>


## Reference(s): <br>
- [LLM Router on ClawHub](https://clawhub.ai/baofeng-tech/llm-router) <br>
- [baofeng-tech publisher profile](https://clawhub.ai/user/baofeng-tech) <br>
- [AIsa API endpoint](https://api.aisa.one/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY for AIsa-backed API calls; the bundled models command can run without an API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
