## Description: <br>
ModelSense recommends the best LLM model and effort level for a task based on benchmark data, task analysis, and the user's configured providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinbenlv](https://clawhub.ai/user/xinbenlv) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and other agent users use this skill when they need help choosing a capable model, effort level, and provider setup for coding, reasoning, writing, research, math, or long-context tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence the active session model or delegate work without consistently requiring user confirmation. <br>
Mitigation: Require explicit user confirmation before any model switch or sub-agent delegation, then state what changed and why. <br>
Risk: Recommendations may rely on benchmark, pricing, or provider-availability data that has changed since the bundled catalog was updated. <br>
Mitigation: Check the user's configured providers and current model availability before applying a recommendation. <br>


## Reference(s): <br>
- [ModelSense README](README.md) <br>
- [Benchmark data](data/benchmarks.yaml) <br>
- [Model catalog](data/models.yaml) <br>
- [OpenRouter model API](https://openrouter.ai/api/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown recommendation with model, effort level, rationale, cost estimate, and alternatives] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model-switch or delegation guidance when the user explicitly asks to apply the recommendation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
