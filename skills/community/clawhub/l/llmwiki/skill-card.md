## Description: <br>
Llmwiki is an LLM-powered personal knowledge base that compiles raw documents into structured, interlinked trilingual wiki articles with emergent taxonomy and self-healing, served through CLI, HTTP, and MCP workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hosuke](https://clawhub.ai/user/hosuke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use Llmwiki to ingest local files, PDFs, and URLs into a personal knowledge base, compile them into linked multilingual wiki articles, and search or query that knowledge through CLI, HTTP, or MCP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires user-supplied LLM credentials and sends content to the configured LLM endpoint. <br>
Mitigation: Use a dedicated API key with usage limits and configure only trusted OpenAI-compatible endpoints. <br>
Risk: Ingested documents, URLs, and Q&A content may be stored locally and used in later wiki compilation or query workflows. <br>
Mitigation: Ingest only content that is appropriate to store locally and process through the selected LLM provider. <br>
Risk: Optional web, API, MCP, and autonomous worker modes add network, file, and mutating-operation exposure in the runtime environment. <br>
Mitigation: Keep optional servers and the worker restricted to trusted environments, and apply binding, proxy, and authentication controls before public exposure. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hosuke/llmwiki) <br>
- [Project homepage](https://github.com/Hosuke/llmbase) <br>
- [Demo](https://huazangge-production.up.railway.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON or YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CLI, HTTP, and MCP usage guidance for local wiki ingest, compile, query, lint, export, and server workflows.] <br>

## Skill Version(s): <br>
0.8.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
