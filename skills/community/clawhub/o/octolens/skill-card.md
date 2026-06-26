## Description: <br>
Query and analyze brand mentions from Octolens API. Use when the user wants to fetch mentions, track keywords, filter by source platforms (Twitter, Reddit, GitHub, LinkedIn, etc.), sentiment analysis, or analyze social media engagement. Supports complex filtering with AND/OR logic, date ranges, follower counts, and bookmarks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garrrikkotua](https://clawhub.ai/user/garrrikkotua) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, marketing teams, and support operators use this skill to query Octolens for brand mentions, saved views, keyword results, sentiment, engagement, and platform-specific filters. It helps agents turn Octolens API responses into focused social listening and product feedback analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Octolens Bearer token and may expose account data if credentials or exported results are mishandled. <br>
Mitigation: Use a least-privileged or read-only API key, avoid passing real keys in command-line history when possible, and do not commit exported results. <br>
Risk: The bundled script documentation includes an optional remote Node.js installer command that uses sudo. <br>
Mitigation: Install Node.js through a trusted package source already approved for the environment, or review the installer source before running it. <br>


## Reference(s): <br>
- [Octolens Skill Page](https://clawhub.ai/garrrikkotua/octolens) <br>
- [Octolens API Usage Examples](references/EXAMPLES.md) <br>
- [Octolens Filter Reference Guide](references/FILTERS.md) <br>
- [Octolens API Scripts](scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the Octolens API and return formatted JSON results, query plans, filters, and summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
