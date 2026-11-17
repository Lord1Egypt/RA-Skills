## Description:

Openclaw Search Pro helps agents run multi-engine web searches and extract web page content using free search engines with optional API-backed providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamwg2025](https://clawhub.ai/user/williamwg2025)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to gather current web results, compare sources across search engines, and extract readable page text for research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and extracted URLs are sent to external search or API providers.

Mitigation: Avoid sensitive queries and install only in contexts where sending this data to external providers is acceptable.

Risk: URL extraction may expose internal-network information when used on untrusted links or in sensitive networks.

Mitigation: Avoid extracting untrusted URLs in sensitive networks and rely on review of the skill's URL validation behavior before deployment.

Risk: API keys may be configured locally for optional providers.

Mitigation: Prefer environment variables for API keys and restrict any configuration file containing credentials.

Risk: Bundled npm dependencies may become outdated or require review before use.

Mitigation: Review and update npm dependencies before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/williamwg2025/skills/openclaw-search-pro)
- [README_EN.md](README_EN.md)
- [BAIDU-API-GUIDE.md](BAIDU-API-GUIDE.md)
- [Baidu Search API](https://ai.baidu.com/tech/search)
- [Baidu AI Search API Documentation](https://ai.baidu.com/ai-doc/SEARCH)
- [Microsoft Bing Web Search API](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and command-line text with search result titles, URLs, snippets, and extracted page summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include third-party URLs and snippets from external search providers; URL extraction prints a summarized text excerpt.]

## Skill Version(s):

0.1.6 (source: ClawHub release evidence, created 2026-03-20T01:26:02Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
