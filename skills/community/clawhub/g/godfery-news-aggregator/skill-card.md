## Description: <br>
Aggregates domestic and international society, technology, and military news, then searches, filters, organizes, and summarizes key points. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect current news from defined technology, military, and society sources and produce structured summaries for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News queries and retrieved search-result text are sent to SkillBoss for processing. <br>
Mitigation: Avoid including private, internal, or sensitive material in queries or summarization prompts. <br>
Risk: The skill requires a sensitive SkillBoss API credential. <br>
Mitigation: Use a dedicated, rotatable SKILLBOSS_API_KEY with the minimum access needed for this workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kirkraman/godfery-news-aggregator) <br>
- [Skill Source Artifact](artifact/SKILL.md) <br>
- [SkillBoss API Hub Endpoint](https://api.skillbossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown news summaries with titles, links, source, time, and key points.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends news queries and retrieved result text to SkillBoss for search and summarization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
