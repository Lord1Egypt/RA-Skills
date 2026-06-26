## Description: <br>
Aggregates domestic and international society, technology, and military news by searching, filtering, and organizing key points. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect current society, technology, and military news, remove duplicates or lower-confidence sources, and produce a structured Markdown briefing with titles, links, sources, timestamps, and key points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News search queries and retrieved snippets are sent to SkillBoss for processing, which may expose sensitive topics or proprietary material. <br>
Mitigation: Use a limited SkillBoss API key, review the provider's privacy and billing expectations, and avoid submitting secrets, internal topics, or proprietary material. <br>
Risk: Aggregated news summaries can include incorrect, outdated, duplicated, or lower-confidence reporting. <br>
Mitigation: Review source links and prioritize official media or authoritative institutions before relying on the briefing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/modestyrichards/modesty-news-aggregator) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [SkillBoss API endpoint](https://api.skillboss.co/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown news briefing with categorized lists and source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends search queries plus retrieved snippets to SkillBoss for search and summarization.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
