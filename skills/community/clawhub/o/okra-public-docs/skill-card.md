## Description: <br>
Query pre-extracted public documents via OkraPDF MCP - arxiv AI papers, SEC 10-K/10-Q filings, and more. Read, ask questions, extract structured data. No upload needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steventsao](https://clawhub.ai/user/steventsao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, analysts, and developers use this skill to configure OkraPDF MCP access and query pre-extracted public arXiv papers or SEC filings for reading, cited Q&A, cross-company comparisons, and structured extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document questions, document IDs, and API-key-backed requests may be sent to OkraPDF. <br>
Mitigation: Use the skill only with prompts and document queries approved for OkraPDF, and avoid confidential research or business prompts unless authorized. <br>
Risk: SEC page verification actions can approve or flag shared extraction-quality state. <br>
Mitigation: Use SEC verification tools only when authorized to make quality-control changes, and review the target document ID and action before running them. <br>


## Reference(s): <br>
- [OkraPDF](https://okrapdf.com) <br>
- [OkraPDF authenticated MCP endpoint](https://api.okrapdf.com/mcp) <br>
- [OkraPDF SEC MCP endpoint](https://mcp.okrapdf.com/mcp) <br>
- [arXiv cs.AI RSS feed](https://rss.arxiv.org/rss/cs.AI) <br>
- [Semantic Scholar paper search API](https://api.semanticscholar.org/graph/v1/paper/search?query=agentic+RAG&year=2026&fields=externalIds,title,citationCount&limit=10) <br>
- [Papers With Code paper search API](https://paperswithcode.com/api/v1/papers/?q=agentic+RAG&items_per_page=5) <br>
- [ClawHub skill page](https://clawhub.ai/steventsao/okra-public-docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets and MCP tool outputs that may include cited answers, extracted document text, and structured JSON data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public document IDs, arXiv IDs, ticker symbols, filing slugs, user questions, page ranges, and optional JSON schemas as inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
