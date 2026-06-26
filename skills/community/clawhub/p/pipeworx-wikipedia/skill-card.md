## Description: <br>
Search, summarize, and explore the structure of English Wikipedia articles with full-text search, section details, and random article retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover Wikipedia articles, retrieve concise article summaries, inspect section structure, and fetch random articles through the Pipeworx Wikipedia MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runtime configuration may request permissions or environment variables outside the static artifact evidence. <br>
Mitigation: Review any permissions or environment variables requested at runtime and avoid providing secrets unless they are clearly required for the task. <br>
Risk: The skill retrieves remote Wikipedia content that may be incomplete, outdated, or unsuitable for a high-stakes answer on its own. <br>
Mitigation: Review returned article links and supporting context before using the output for factual or user-facing conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-wikipedia) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces article search results, summaries, section metadata, random article extracts, and MCP configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
