## Description: <br>
AI Agent search platform with 9 engines, Google 13 sub-types, vertical scene search, and intelligent auto/multi/extract modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goldentrii](https://clawhub.ai/user/goldentrii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to run multi-engine web search, URL extraction, and scene-specific queries, then consume structured results for planning, comparison, research, and downstream automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, URLs, and selected research-result URLs are sent to Novada services. <br>
Mitigation: Avoid secrets, internal-only links, authenticated pages, regulated data, and proprietary identifiers in queries or extraction URLs. <br>
Risk: The skill requires a Novada API key for search and extraction calls. <br>
Mitigation: Use least-privilege environment setup and avoid logging or sharing the NOVADA_API_KEY value. <br>
Risk: The action-links output format can print shell commands. <br>
Mitigation: Review any generated command before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goldentrii/novada-search) <br>
- [Novada project homepage](https://novada.com) <br>
- [Novada Search repository](https://github.com/NovadaLabs/novada-search) <br>
- [Novada Search README](https://github.com/NovadaLabs/novada-search#readme) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration] <br>
**Output Format:** [JSON, Markdown tables and lists, shell commands, or raw API responses depending on the selected output format.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOVADA_API_KEY for search and extraction calls; agent-json output includes structured search metadata and unified results.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata, SKILL.md frontmatter, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
