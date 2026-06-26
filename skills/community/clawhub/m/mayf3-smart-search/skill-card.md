## Description: <br>
Smart Search helps agents run multi-engine web searches with language-aware fallback, structured result parsing, content extraction, and source quality guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mayf3](https://clawhub.ai/user/mayf3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to gather web information, compare search results across engines, extract readable content from URLs, and assess source credibility for market research, technical lookup, news search, and fact checking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and URLs may be sent to external search engines or remote extraction services. <br>
Mitigation: Do not use the skill with secrets, private or internal URLs, proprietary project names, or regulated data unless that external disclosure is acceptable. <br>
Risk: URL extraction can request user-supplied URLs from environments that may have access to internal services. <br>
Mitigation: Use --extract-url only for public URLs or run the skill in an environment with network controls that block internal address ranges. <br>
Risk: Search results and extracted content can be stale, incomplete, or misleading. <br>
Mitigation: Cross-check important claims with multiple authoritative sources and apply the included credibility assessment guidance. <br>


## Reference(s): <br>
- [Advanced Search Syntax](references/advanced-syntax.md) <br>
- [Search Result Credibility Assessment](references/credibility-assessment.md) <br>
- [Search API Upgrade Paths](references/search-apis.md) <br>
- [Vertical Search Routing](references/vertical-search.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mayf3/mayf3-smart-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, Python, and JSON examples; optional JSON or URL-only command output from the bundled search script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output may include titles, URLs, snippets, extracted full text, news, images, videos, books, or batch results depending on the selected command options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
