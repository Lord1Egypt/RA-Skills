## Description: <br>
Helps agents initialize PDFs, inspect document outlines, search text or semantics, read selected pages, and extract figures or tables with the doc-search CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rise-1210](https://clawhub.ai/user/rise-1210) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer questions about PDF documents, locate relevant pages or topics, extract structured evidence from figures and tables, and avoid full-document scans when targeted search is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDFs and derived images or text may be sent to configured MinerU or other API endpoints, and the security summary notes that a public remote service may be used by default. <br>
Mitigation: Use the skill only for documents approved for those endpoints, or change config.yaml to local mode or remove server_url before handling confidential documents. <br>
Risk: Optional external services can require API keys for PageIndex, embedding, reranking, or MinerU cloud features. <br>
Mitigation: Enter API keys only when the feature is needed and store them in the documented configuration or environment variables rather than embedding them in prompts or shared outputs. <br>
Risk: The bundled tooling can run a local FastAPI server. <br>
Mitigation: Do not start the server unless the bind address and authentication settings are understood and acceptable for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rise-1210/mineru-document-explorer) <br>
- [Installation and configuration](references/setup.md) <br>
- [Initialize a PDF](references/cmd-init.md) <br>
- [Browse document structure](references/cmd-outline.md) <br>
- [Read pages](references/cmd-pages.md) <br>
- [Regex keyword search](references/cmd-search-keyword.md) <br>
- [Semantic search](references/cmd-search-semantic.md) <br>
- [Evidence extraction](references/cmd-elements.md) <br>
- [Workflows and lessons learned](references/tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local page images or cropped evidence files produced by the PDF search tooling.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
