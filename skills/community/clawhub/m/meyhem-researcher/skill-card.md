## Description: <br>
Multi-query research tool with LLM-ranked results and freshness control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c5huracan](https://clawhub.ai/user/c5huracan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and research-oriented agents use this skill to break a topic into multiple focused web research queries, retrieve LLM-ranked results, and preview selected result content without managing an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries, agent identifiers, and selected result URLs are transmitted to api.rhdxm.com. <br>
Mitigation: Avoid submitting confidential investigations, proprietary plans, secrets, customer data, or regulated personal information unless the provider's data handling is approved for that use. <br>
Risk: Search results and previews may be incomplete, stale, or misleading despite LLM ranking and freshness controls. <br>
Mitigation: Treat returned results as research leads and verify important claims against primary or trusted sources before relying on them. <br>


## Reference(s): <br>
- [Meyhem API Docs](https://api.rhdxm.com/docs) <br>
- [Meyhem MCP Endpoint](https://api.rhdxm.com/mcp/) <br>
- [ClawHub Skill Page](https://clawhub.ai/c5huracan/meyhem-researcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown-style console output containing generated queries, ranked result titles, URLs, and short previews.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on api.rhdxm.com availability, selected freshness, requested result count, query count, and transmitted agent identifier.] <br>

## Skill Version(s): <br>
0.2.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
