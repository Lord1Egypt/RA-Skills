## Description:

Query pre-extracted public documents via OkraPDF MCP, including arXiv AI papers and SEC 10-K/10-Q filings, to read documents, ask questions, and extract structured data without uploading files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steventsao](https://clawhub.ai/user/steventsao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to configure OkraPDF MCP services and query pre-indexed public research papers and SEC filings. It supports document reading, cited question answering, cross-company filing comparisons, and JSON-schema-based data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Questions and extraction prompts are sent to OkraPDF MCP services.

Mitigation: Install only when the user trusts those services and is comfortable sharing the relevant prompts and document-query context with them.

Risk: The SEC workflow includes page approval and flagging actions that can change shared extraction-quality metadata.

Mitigation: Treat verification tools as administrative actions and require explicit human approval before an agent calls verify_pages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/steventsao/skills/okra-public-docs)
- [OkraPDF](https://okrapdf.com)
- [OkraPDF authenticated MCP endpoint](https://api.okrapdf.com/mcp)
- [OkraPDF SEC MCP endpoint](https://mcp.okrapdf.com/mcp)
- [papers.json manifest](papers.json)
- [Example arXiv PDF](https://arxiv.org/pdf/2603.26653)
- [arXiv cs.AI RSS feed](https://rss.arxiv.org/rss/cs.AI)
- [arXiv cs.CL RSS feed](https://rss.arxiv.org/rss/cs.CL)
- [arXiv cs.LG RSS feed](https://rss.arxiv.org/rss/cs.LG)
- [Semantic Scholar paper search API](https://api.semanticscholar.org/graph/v1/paper/search?query=agentic+RAG&year=2026&fields=externalIds,title,citationCount&limit=10)
- [Papers With Code paper search API](https://paperswithcode.com/api/v1/papers/?q=agentic+RAG&items_per_page=5)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets, shell command examples, cited answers, and optional structured JSON extraction output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include document identifiers, page ranges, questions, ticker lists, filing selectors, and JSON schemas for extraction.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
