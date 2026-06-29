## Description: <br>
Helps researchers expand a topic into real-time Google Scholar searches, deduplicate candidate papers, and rank the results with venue-quality signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[figpad](https://clawhub.ai/user/figpad) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Researchers, graduate students, academic writers, and developers use this skill to turn a research topic or seed paper into a Google Scholar literature search and a ranked reading table. It is useful when a user needs transparent search queries, source evidence, venue-quality tags, access links, and concise reasons for keeping or checking each paper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries and retrieved paper metadata flow through the connected Google Scholar MCP server. <br>
Mitigation: Use the skill only with a trusted Scholar MCP server, and report when the server is unavailable, blocked, rate-limited, or returns no usable data. <br>
Risk: Venue metrics, citation counts, access links, and local quality data may be incomplete or outdated. <br>
Mitigation: Treat rankings as literature triage and manually verify important citations, venue details, abstracts, and access links before relying on them. <br>
Risk: Replacing failed Scholar retrieval with model memory or unrelated search sources could create fabricated or misleading paper records. <br>
Mitigation: Fail closed when Google Scholar MCP evidence is unavailable, and clearly label any optional comparison source outside the Google Scholar result table. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/figpad/google-scholar-paper-finder) <br>
- [Search Workflow](references/search-workflow.md) <br>
- [Quality Scoring](references/quality-scoring.md) <br>
- [Venue Quality Data](data/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown table by default, with optional enriched JSON or Markdown files from the scoring script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes search queries used, source labels, candidate-pool counts, dedupe counts, access links, recommendation tiers, ranking reasons, and limitations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
