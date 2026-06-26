## Description: <br>
Searches academic papers through the Semantic Scholar API and returns paper metadata, citation counts, abstracts, links, and optional JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhoujc11](https://clawhub.ai/user/zhoujc11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to search academic literature by topic, year, and citation filters, then retrieve paper metadata or details for follow-up review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries are sent to Semantic Scholar. <br>
Mitigation: Use the skill only when that network disclosure is acceptable; avoid submitting sensitive or confidential research queries. <br>
Risk: The skill name may imply Google Scholar, but the implementation uses Semantic Scholar and may return different coverage or PDF availability. <br>
Mitigation: Treat results as Semantic Scholar metadata and verify important citations, abstracts, and open-access PDF links against the source venue before relying on them. <br>


## Reference(s): <br>
- [Semantic Scholar API Reference](references/API.md) <br>
- [Semantic Scholar](https://www.semanticscholar.org) <br>
- [Semantic Scholar API](https://api.semanticscholar.org) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhoujc11/google-scholar-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with CLI examples; command output as plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns paper titles, authors, years, venues, citation counts, abstracts, Semantic Scholar URLs, paper IDs, and open-access PDF links when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
