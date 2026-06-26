## Description: <br>
List available AI models from OATDA's providers with optional filtering by model type or provider name. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devcsde](https://clawhub.ai/user/devcsde) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to query OATDA for available chat, image, and video models, inspect supported parameters, and choose model identifiers for related OATDA workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OATDA API key from the environment or ~/.oatda/credentials.json. <br>
Mitigation: Use an API key with only the required access, keep the credentials file protected, and do not print or share the full key. <br>
Risk: The skill sends GET requests to OATDA to retrieve model metadata. <br>
Mitigation: Review the requested endpoint and filters before execution and run the commands only when OATDA is trusted for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/devcsde/oatda-list-models) <br>
- [OATDA homepage](https://oatda.com) <br>
- [OATDA models API endpoint](https://oatda.com/api/v1/llm/models) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq with OATDA_API_KEY or ~/.oatda/credentials.json; results should be formatted from live API data rather than hardcoded model names.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
