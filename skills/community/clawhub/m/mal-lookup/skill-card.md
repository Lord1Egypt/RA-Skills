## Description: <br>
Direct MyAnimeList lookup tool. Bypasses Jikan/API issues by using MAL's internal endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zun43d](https://clawhub.ai/user/zun43d) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Anime and manga users, list maintainers, and agents use this skill to search MyAnimeList entries, inspect top or seasonal charts, and retrieve public anime or manga lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup terms and usernames may be sent to MyAnimeList during searches, list retrieval, chart lookups, or seasonal queries. <br>
Mitigation: Avoid entering sensitive search text, private identifiers, or usernames that should not be shared with MyAnimeList. <br>
Risk: Results depend on MyAnimeList internal endpoints and may be unavailable or change without notice. <br>
Mitigation: Treat lookup results as external web data and verify important results against MyAnimeList before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zun43d/mal-lookup) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and text results from MyAnimeList lookups] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, grep, and awk; lookup terms and usernames may be sent to MyAnimeList.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata; artifact frontmatter is 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
