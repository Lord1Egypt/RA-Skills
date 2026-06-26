## Description: <br>
Aggregates Chinese hot-topic and news trend data from Zhihu, Toutiao, and AIBase, with commands for single-platform fetches, all-platform collection, status checks, and cross-platform keyword comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sskun](https://clawhub.ai/user/sskun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve current Chinese hot-search, news, and AI news lists from supported public platforms and to compare repeated keywords across platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches live public web content from third-party platforms, so responses may include inaccurate, changing, or unavailable data. <br>
Mitigation: Treat results as current third-party content, check platform status output when data is missing, and verify important claims against the original linked source. <br>
Risk: AIBase article content may include untrusted HTML returned from a third-party site. <br>
Mitigation: Render or summarize returned HTML as untrusted content and sanitize it before displaying it in any downstream UI. <br>
Risk: Dependency ranges are not pinned exactly, which can reduce reproducibility across installations. <br>
Mitigation: Install in a virtual environment and pin or audit dependencies when reproducible or controlled deployments are required. <br>
Risk: Authenticated Zhihu features described in reference material may require session cookies if deliberately enabled or extended. <br>
Mitigation: Protect any Zhihu cookies as session credentials and avoid exporting or sharing them unless the authenticated workflow is explicitly needed. <br>


## Reference(s): <br>
- [Architecture](references/architecture.md) <br>
- [Data Schema](references/data-schema.md) <br>
- [Platform Guide](references/platform-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, JSON Lines, and concise Markdown guidance with shell commands when the agent invokes the CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetch and all commands return per-platform JSON payloads; compare returns keyword-frequency analysis with top_keywords and per_platform fields.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
