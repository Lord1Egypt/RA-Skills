## Description: <br>
Intelligent search for agents. Multi-source retrieval with confidence scoring - web, academic, and Tavily in one unified API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and research agents use this skill to run web, academic, smart, full-text, and Tavily-backed searches, then compare source coverage and confidence for research, market analysis, news aggregation, and technical due diligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, URLs, retrieved page content, or result summaries may be sent to AIsa and its search backends. <br>
Mitigation: Use the skill only for data appropriate for external processing, and avoid secrets, private documents, authenticated pages, internal systems, and regulated data. <br>
Risk: The API key can authorize paid external API usage. <br>
Mitigation: Use a dedicated, revocable AISA_API_KEY and monitor usage or billing. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/0xjordansg-yolo/openclaw-aisa-search-website-academic-tavily-serp-exa) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [AIsa API documentation](https://aisa.mintlify.app) <br>
- [AIsa Verity reference implementation](https://github.com/AIsa-team/verity) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash examples and JSON API or client results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl or python3 and an AISA_API_KEY; search terms, URLs, retrieved content, and result summaries may be sent to AIsa APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
