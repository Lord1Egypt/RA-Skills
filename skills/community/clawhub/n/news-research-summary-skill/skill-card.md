## Description: <br>
Researches news and factual information on the web, then produces a cited, deduplicated summary tailored to constraints such as topic, time range, region, sources, language, length, and angle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darinouyang](https://clawhub.ai/user/darinouyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and employees use this skill to research current news, policy, competitive, industry, or factual topics on the public web and receive concise summaries with citations, deduplication, source quality checks, and clear separation of fact from analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News and factual summaries may contain source errors, stale information, or unverified single-source claims. <br>
Mitigation: Review important cited claims directly, prefer primary sources, and label single-source or conflicting claims as required by the skill guidance. <br>
Risk: The skill may produce Chinese section headings or bilingual query behavior when that does not fit the deployment context. <br>
Mitigation: Adapt the output language and template headings to the user or product context before publishing results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/darinouyang/news-research-summary-skill) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [examples.md](artifact/examples.md) <br>
- [reference.md](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summary with source links, key points, details, optional impact assessment, source list, and search notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cited factual bullets, deduplicated stories, labeled single-source or conflicting claims, and output language matched to the user when possible] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
