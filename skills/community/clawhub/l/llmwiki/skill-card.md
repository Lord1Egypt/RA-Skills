## Description:

Llmwiki helps agents and users turn raw documents into a local, LLM-compiled knowledge base with interlinked trilingual wiki articles, emergent taxonomy, querying, and CLI, HTTP, and MCP access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hosuke](https://clawhub.ai/user/hosuke)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use Llmwiki to build, query, and maintain a personal knowledge base from local files, URLs, PDFs, and corpus plugins. Agents can connect through MCP or HTTP to search compiled concepts, inspect raw sources, ingest new material, compile wiki pages, lint the knowledge graph, and export structured content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional web or API server can permit unauthenticated persistent writes if exposed on a shared or public network.

Mitigation: Bind services to localhost or place them behind authentication, a reverse proxy, and rate limits before exposing them beyond a trusted environment.

Risk: The install command pulls external package code without pinning a version.

Mitigation: Install in an isolated environment and pin the package version during deployment.

Risk: Documents provided for compilation or question answering may be sent to the configured LLM API.

Mitigation: Use an approved OpenAI-compatible endpoint and avoid ingesting sensitive documents unless that endpoint is authorized for the data.

## Reference(s):

- [Llmwiki ClawHub skill page](https://clawhub.ai/hosuke/skills/llmwiki)
- [Publisher profile](https://clawhub.ai/user/hosuke)
- [llmbase GitHub repository](https://github.com/Hosuke/llmbase)
- [Hosted demo](https://huazangge-production.up.railway.app)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON snippets, and YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include MCP server configuration, CLI commands, setup guidance, operational workflows, and generated or updated local wiki markdown.]

## Skill Version(s):

0.8.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
