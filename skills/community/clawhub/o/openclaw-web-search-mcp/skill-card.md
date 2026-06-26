## Description: <br>
Provides AI agents with web search, page and PDF extraction, YouTube transcripts, summarization, semantic search, and automated research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nishant-clawit](https://clawhub.ai/user/nishant-clawit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this MCP skill to let agents search the web, extract content from pages and PDFs, retrieve YouTube transcripts, summarize text, store searchable text, and run multi-step research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A transcript tool can pass a user-supplied URL into a local shell command. <br>
Mitigation: Review before installing; use only trusted inputs, replace shell command construction with argument-array execution or a safer transcript library, and avoid passing internal or sensitive URLs. <br>
Risk: Search queries and fetched web content are sent to external sites. <br>
Mitigation: Do not pass secrets in search queries or web content, validate or allowlist URLs, and add request limits before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nishant-clawit/openclaw-web-search-mcp) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [MCP tool manifest](artifact/mcp.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool outputs may include external search results, extracted text capped by the artifact, transcript segments, summaries, embedding storage status, semantic search matches, and research findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
