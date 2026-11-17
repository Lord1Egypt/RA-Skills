## Description:

Research and compare news from the Chinng AI-Agent Portal. Use when finding relevant articles, investigating a topic, or preparing a sourced news summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinng-inta](https://clawhub.ai/user/chinng-inta)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users performing news research use this skill to find, compare, and cite relevant portal records while preserving original source links and respecting omitted content metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote Chinng AI-Agent Portal MCP service can change independently of the reviewed skill.

Mitigation: Confirm the endpoint before installation, treat portal results as a research aid, and retain original source links.

Risk: News metadata and entity hints may be incomplete or imprecise, especially for link-only records.

Mitigation: Use metadata for triage, retrieve only records that materially improve the answer, and do not reconstruct content withheld by the portal.

## Reference(s):

- [Chinng AI-Agent Portal MCP endpoint](https://portal.chinng-lab-srv.dev/mcp)
- [ClawHub skill page](https://clawhub.ai/chinng-inta/skills/news-triage)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with citations and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dated news pointers, comparison notes, and concise sourced summaries.]

## Skill Version(s):

0.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
