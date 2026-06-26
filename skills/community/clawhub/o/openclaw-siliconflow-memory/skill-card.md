## Description: <br>
Configure OpenClaw semantic memory to use SiliconFlow embeddings through an OpenAI-compatible API, especially BAAI/bge-m3, and validate memory indexing and retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[otweihan](https://clawhub.ai/user/otweihan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure OpenClaw memory_search with SiliconFlow embeddings, add curated Markdown knowledge paths, and validate indexing and retrieval through CLI and tool-layer checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SiliconFlow API keys can be exposed if users paste secrets into shared configuration or logs. <br>
Mitigation: Review the configuration patch before applying it, keep the API key private, and avoid sharing logs or files that contain credentials. <br>
Risk: Adding broad local folders to semantic memory can make unintended personal or noisy files searchable. <br>
Mitigation: Add only curated Markdown folders that the user is comfortable making searchable, and expand extraPaths in small batches. <br>
Risk: A wrong provider, endpoint, model, or fallback setting can hide embedding failures or produce failed retrieval. <br>
Mitigation: Keep provider, model, baseUrl, apiKey, and fallback explicit, then validate with memory status, forced indexing, CLI search, and tool-layer retrieval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/otweihan/openclaw-siliconflow-memory) <br>
- [SiliconFlow OpenAI-compatible API endpoint](https://api.siliconflow.cn/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes validation steps for OpenClaw memory status, indexing, and search.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
