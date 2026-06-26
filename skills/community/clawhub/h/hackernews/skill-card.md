## Description: <br>
Browse and search Hacker News, including story lists, item details, comments, user profiles, Algolia search results, and "Who is hiring?" threads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gchapim](https://clawhub.ai/user/gchapim) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and external users can use this skill to browse public Hacker News content, inspect comments and user profiles, search posts or comments, and find current hiring threads from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and requested Hacker News identifiers are sent to public Hacker News and Algolia APIs. <br>
Mitigation: Avoid entering sensitive private terms or confidential identifiers in HN searches or lookups. <br>
Risk: The CLI depends on local tools and network access to public APIs. <br>
Mitigation: Confirm curl, jq, and python3 are installed and review commands before execution in restricted environments. <br>


## Reference(s): <br>
- [Hacker News API Reference](references/api.md) <br>
- [Hacker News Firebase API](https://hacker-news.firebaseio.com/v0/) <br>
- [Algolia Hacker News Search API](https://hn.algolia.com/api/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Plain text or JSON returned by CLI commands, commonly summarized by the agent in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public API results; commands support configurable limits, filters, and raw JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
