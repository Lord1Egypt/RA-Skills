## Description: <br>
多搜索聚合器 aggregates search results from Tavily, Brave, and Perplexity into unified Markdown or JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lirun26](https://clawhub.ai/user/lirun26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run a web search across configured Tavily, Brave, and Perplexity providers and collect standardized results for downstream review or summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to configured third-party search providers under the user's API keys. <br>
Mitigation: Avoid queries containing secrets, credentials, sensitive personal data, or private project names, and configure only the providers intended for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lirun26/multi-search-aggregator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, or unified JSON from command-line execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires at least one configured provider API key; default sources are Tavily and Brave.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, artifact metadata, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
