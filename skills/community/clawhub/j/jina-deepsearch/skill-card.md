## Description:

Jina DeepSearch API access via AIHubMix - use curl to call the HTTP API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ansatzx](https://clawhub.ai/user/ansatzx)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to configure AIHUBMIX_API_KEY and call Jina DeepSearch through AIHubMix with curl for search-oriented chat completion requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and search queries are sent to AIHubMix's Jina DeepSearch API.

Mitigation: Use the skill only when AIHubMix is an intended provider and avoid submitting secrets or sensitive personal data unless account terms and provider policies allow it.

Risk: The API key is supplied through the AIHUBMIX_API_KEY environment variable.

Mitigation: Keep AIHUBMIX_API_KEY private, avoid logging it, and rotate it if exposure is suspected.

## Reference(s):

- [Jina AI](https://jina.ai/)
- [AIHubMix](https://aihubmix.com)
- [AIHubMix Chat Completions Endpoint](https://aihubmix.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and the AIHUBMIX_API_KEY environment variable.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
