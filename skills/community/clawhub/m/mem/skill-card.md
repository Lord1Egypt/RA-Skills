## Description: <br>
Search local memory index (local-first). Use for /mem queries in Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Trumppo](https://clawhub.ai/user/Trumppo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to search a cached local memory index for /mem queries and return relevant paths, headers, and brief summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on local helper scripts that are not included in the package. <br>
Mitigation: Verify that scripts/index-memory.py and scripts/search-memory.py on the target machine are trusted before invoking the skill. <br>
Risk: The local memory index may contain secrets or private folders that should not be summarized in chat. <br>
Mitigation: Review the indexed locations and exclude sensitive content before running searches or sharing summarized results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Trumppo/mem) <br>
- [Publisher profile](https://clawhub.ai/user/Trumppo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns top memory hits with paths and headers; summaries should avoid exposing unnecessary private content.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
