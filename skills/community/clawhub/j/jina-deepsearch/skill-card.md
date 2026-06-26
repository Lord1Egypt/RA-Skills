## Description: <br>
Jina DeepSearch API access via AIHubMix - use curl to call the HTTP API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ansatzX](https://clawhub.ai/user/ansatzX) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to configure an AIHubMix API key and call Jina DeepSearch with curl for search-oriented chat completions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AIHubMix API key and sends search prompts to AIHubMix/Jina. <br>
Mitigation: Use a limited-purpose API key, monitor quota or billing, and avoid including secrets or sensitive private data in prompts. <br>
Risk: The skill gives direct curl usage guidance for an external HTTP API. <br>
Mitigation: Review commands before running them and confirm the endpoint, model, and headers match the intended environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ansatzX/jina-deepsearch) <br>
- [Jina homepage](https://jina.ai/) <br>
- [AIHubMix](https://aihubmix.com) <br>
- [AIHubMix chat completions endpoint](https://aihubmix.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and AIHUBMIX_API_KEY; search prompts are sent to AIHubMix/Jina.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
