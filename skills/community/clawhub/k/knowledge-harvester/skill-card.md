## Description: <br>
Daily automated briefings that fetch trending content via Google News RSS and summarize it into memory for RAG retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dainash](https://clawhub.ai/user/dainash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain a configurable, attributed stream of summarized news articles for later retrieval. It is intended for agents that need recurring domain-specific briefings stored as Markdown knowledge files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured topics are sent to Google News as search queries. <br>
Mitigation: Avoid sensitive interests in domains.md and review configured domains before running the skill. <br>
Risk: Generated summaries are stored in persistent memory and may influence future retrieval. <br>
Mitigation: Periodically review or prune memory/knowledge to remove stale or unwanted summaries. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dainash/knowledge-harvester) <br>
- [Publisher profile](https://clawhub.ai/user/dainash) <br>
- [Google News RSS search endpoint](https://news.google.com/rss/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown knowledge files with YAML frontmatter and brief run summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes attributed 100-200 word article summaries to memory/knowledge and can create a default domain configuration in memory/clawforage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
