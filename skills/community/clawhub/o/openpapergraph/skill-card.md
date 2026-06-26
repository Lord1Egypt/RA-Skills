## Description: <br>
OpenPaperGraph supports academic literature discovery and citation network analysis through multi-source paper search, citation graph construction, recommendations, monitoring, PDF parsing, Zotero import, research summaries, exports, and interactive HTML graph visualizations. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[jiahaowugit](https://clawhub.ai/user/jiahaowugit) <br>

### License/Terms of Use: <br>
PolyForm Noncommercial License 1.0.0 <br>


## Use Case: <br>
Researchers, students, and developer-facing research assistants use this skill to search academic literature, build and inspect citation graphs, summarize research areas, import Zotero or PDF references, and export results for review or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The interactive graph server can expose unauthenticated graph-changing actions if reachable from untrusted networks. <br>
Mitigation: Run server mode only in a trusted local environment, prefer localhost-only isolation, and avoid exposing the port publicly. <br>
Risk: Graph editing commands can persistently modify graph JSON files. <br>
Mitigation: Keep backups or work on copies before using server mode, seed removal, or graph management commands. <br>
Risk: Search, citation, PDF, Zotero, and summary workflows can send queries, paper metadata, PDFs, or prompts to external services. <br>
Mitigation: Do not provide sensitive API keys, private manuscripts, or confidential research data unless the selected provider is approved for that data. <br>


## Reference(s): <br>
- [ClawHub OpenPaperGraph release page](https://clawhub.ai/jiahaowugit/openpapergraph) <br>
- [Semantic Scholar API](https://www.semanticscholar.org/product/api) <br>
- [GROBID](https://github.com/kermitt2/grobid) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [JSON stdout plus optional Markdown, BibTeX, CSV, HTML, and graph JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external scholarly APIs and optional LLM providers; some commands persist changes to local graph JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
