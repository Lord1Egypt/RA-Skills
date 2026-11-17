## Description:

Intelligent search for agents. Multi-source retrieval with confidence scoring - web, academic, and Tavily in one unified API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to retrieve web, academic, smart-search, and Tavily-backed results through one AIsa API workflow and to produce confidence-scored search outputs for research, market analysis, news aggregation, and competitive analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, URL targets, retrieved result sets, and crawl or site-map requests are sent to the AIsa API and Tavily-backed endpoints.

Mitigation: Do not use the skill with secrets, confidential internal research, private URLs, localhost, internal network hosts, or access-controlled pages unless the organization has approved that data sharing.

Risk: The skill can request extraction, crawling, and site maps for user-supplied URLs.

Mitigation: Restrict URL inputs to public, approved targets and review crawl or extraction requests before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xjordansg-yolo/skills/openclaw-aisa-search-website-academic-tavily-serp-exa)
- [OpenClaw Homepage](https://openclaw.ai)
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction)
- [AIsa Documentation](https://aisa.mintlify.app)
- [AIsa Verity Reference Implementation](https://github.com/AIsa-team/verity)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, Python examples, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and network access to AIsa API endpoints; responses may include confidence scores, source breakdowns, usage cost, and remaining credits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
