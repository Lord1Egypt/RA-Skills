## Description:

OpenClaw Search helps agents retrieve web, academic, and Tavily-backed results through AIsa APIs with confidence scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run web, academic, hybrid, full-text, Tavily, and multi-source searches via AIsa APIs, then inspect JSON results with confidence scoring for research, market analysis, competitive analysis, and news aggregation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search, extract, crawl, map, and explain operations send queries, URLs, and result data to external AIsa/Tavily-backed services.

Mitigation: Use only organization-approved queries, URLs, and documents, and avoid submitting secrets, proprietary project terms, internal URLs, authenticated pages, or private documents.

Risk: The skill requires an AISA_API_KEY for API access.

Mitigation: Provide the key through an approved environment or secret-management path and avoid exposing it in prompts, logs, screenshots, or shared command output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aisadocs/skills/openclaw-aisa-search-web-academic-tavily)
- [OpenClaw Homepage](https://openclaw.ai)
- [AIsa Documentation](https://aisa.mintlify.app)
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction)
- [AIsa Verity](https://github.com/AIsa-team/verity)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and sends search queries, URLs, and result data to external AIsa/Tavily-backed services.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
