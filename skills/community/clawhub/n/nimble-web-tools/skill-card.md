## Description: <br>
Nimble Real-Time Web Intelligence Tools guides agents to use the Nimble CLI for live web search, content extraction, site mapping, and crawling with structured outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilchemla](https://clawhub.ai/user/ilchemla) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI agents use this skill to route web research, current information lookup, URL extraction, site mapping, and bulk crawling tasks through the Nimble CLI. It is suited for workflows that need clean JSON, YAML, markdown, or raw web intelligence outputs from a third-party Nimble account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes broad web research, extraction, mapping, and crawling tasks through a third-party Nimble service using the user's API key. <br>
Mitigation: Install only when Nimble should handle web research, use a dedicated API key, avoid logging or sharing the key, and monitor quota usage. <br>
Risk: Bulk crawling can over-collect data, consume quota, or target sites where the user lacks authorization. <br>
Mitigation: Set explicit crawl limits, scope crawl paths carefully, and avoid invasive person-research or unauthorized scraping targets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ilchemla/nimble-web-tools) <br>
- [Publisher profile](https://clawhub.ai/user/ilchemla) <br>
- [Nimbleway agent skills repository](https://github.com/Nimbleway/agent-skills) <br>
- [Search focus modes reference](references/search-focus-modes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples; Nimble CLI outputs may be JSON, YAML, pretty text, raw API data, markdown, plain text, simplified HTML, or HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a pre-installed Nimble CLI and NIMBLE_API_KEY; outputs may route broad web tasks through a third-party Nimble service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
