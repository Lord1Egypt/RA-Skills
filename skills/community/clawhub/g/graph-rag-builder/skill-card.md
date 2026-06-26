## Description: <br>
Builds a runnable MCP knowledge server from a website or documentation URL by crawling content, extracting concepts with Claude, building a knowledge graph, generating embeddings, and producing semantic search and graph traversal tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nacmonad](https://clawhub.ai/user/nacmonad) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to turn public documentation, tutorial sites, or learning materials into Claude-searchable MCP knowledge servers with semantic search and graph traversal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The pipeline can install unpinned Python packages and browser components into the runtime environment. <br>
Mitigation: Run it in a virtual environment or container and review dependency installation steps before execution. <br>
Risk: Crawled content may be sent to Anthropic during concept extraction. <br>
Mitigation: Crawl only content you are allowed to store and send to Anthropic, avoid private or authenticated docs unless explicitly approved, and use a budget-limited API key. <br>
Risk: The generated MCP server and Claude Desktop configuration are executable integration artifacts. <br>
Mitigation: Review generated server.py and mcp_config.json before adding them to Claude Desktop. <br>


## Reference(s): <br>
- [GraphRAGBuilder ClawHub listing](https://clawhub.ai/nacmonad/graph-rag-builder) <br>
- [Strudel workshop sample target](https://strudel.cc/workshop/getting-started/) <br>
- [Anthropic Skills overview](https://www.anthropic.com/news/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands plus generated Python, JSON, graph, and embedding files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides a five-stage local pipeline and produces an output folder containing server.py, mcp_config.json, graph.json, raw content, extracted concepts, and numpy embeddings.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
