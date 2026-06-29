## Description: <br>
Fetches and analyzes the OpenRouter model catalog, including pricing, context length, modalities, provider families, free models, and capability-based comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzfly256](https://clawhub.ai/user/zzfly256) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and analysts use this skill to answer OpenRouter-specific model pricing and capability questions, such as finding the cheapest model with a modality, comparing provider families, or listing free models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Refreshing the catalog contacts OpenRouter and writes a local JSON cache. <br>
Mitigation: Refresh only when current pricing data is needed and treat the resulting cache as the source for analysis until it is refreshed again. <br>
Risk: Supplying an OpenRouter API key attributes requests to the user's account. <br>
Mitigation: Use the public unauthenticated endpoint unless account attribution or higher rate limits are intentionally required. <br>


## Reference(s): <br>
- [OpenRouter models API](https://openrouter.ai/api/v1/models) <br>
- [OpenRouter pricing field reference](references/pricing_fields.md) <br>
- [OpenRouter model families](references/model_families.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus text table, JSON, or statistics output from the analysis script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local cached OpenRouter catalog; refreshes require a network call to OpenRouter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
