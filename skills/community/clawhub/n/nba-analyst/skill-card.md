## Description: <br>
NBA Analyst is a Chinese-language NBA data assistant for scores, standings, player and team statistics, comparisons, AI-style analysis, and visual HTML reports without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer NBA questions in Chinese, including live or historical scores, standings, schedules, player and team lookups, comparisons, and report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests for NBA data and depends on public NBA.com endpoint availability and terms. <br>
Mitigation: Run it only where outbound NBA data access is approved, and expect endpoints to be rate-limited or unavailable at times. <br>
Risk: The skill creates local cache and report files during normal use. <br>
Mitigation: Use a workspace where local cache and generated HTML report files are acceptable, and clean those files when no longer needed. <br>
Risk: Dependency resolution may vary across environments. <br>
Mitigation: Install from a locked environment or pin the listed Python dependencies when reproducibility matters. <br>
Risk: Generic sports queries may trigger this NBA-specific skill even when another sport is intended. <br>
Mitigation: Confirm the user is asking about NBA basketball before relying on the skill's response. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/nba-analyst) <br>
- [Publisher profile](https://clawhub.ai/user/bettermen) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Artifact manifest](artifact/clawhub.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, html, files, guidance] <br>
**Output Format:** [Markdown-style text responses and generated HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local NBA cache files and HTML reports; outputs depend on NBA.com public API availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
