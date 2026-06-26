## Description: <br>
Sift provides web search, research synthesis, fact verification, document summarization, and structured entity extraction with tiered source selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigokarasu](https://clawhub.ai/user/indigokarasu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Sift for web lookups, multi-source research, fact-checking, comparison research, document summarization, and structured extraction of entities, claims, statistics, relationships, and citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a daily self-updater that pulls changes from its source. <br>
Mitigation: Review the updater before installation and prefer disabling the cron job or using manual updates when change control is required. <br>
Risk: The skill stores local journals and extracted research data. <br>
Mitigation: Avoid sensitive research unless the retention settings and local storage location match the user's data handling requirements. <br>
Risk: Selected extracted entities may be shared with another local skill intake. <br>
Mitigation: Review cross-skill sharing behavior and disable or restrict entity emission when the research content should remain isolated. <br>
Risk: Search providers may require API keys and receive query content. <br>
Mitigation: Use limited-purpose search API keys and avoid sending confidential queries to external providers. <br>


## Reference(s): <br>
- [Sift ClawHub Release](https://clawhub.ai/indigokarasu/ocas-sift) <br>
- [README](README.md) <br>
- [Search Tiers](references/search_tiers.md) <br>
- [Schemas](references/schemas.md) <br>
- [Query Rewrite](references/query_rewrite.md) <br>
- [Journal](references/journal.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance] <br>
**Output Format:** [Markdown responses with JSON session, journal, entity, source, decision, and signal records when persistence is enabled] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local research storage, journals, Elephas intake signal files, and a scheduled self-update command.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
