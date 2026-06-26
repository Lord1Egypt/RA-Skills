## Description: <br>
Aggregates multiple search sources with fallback routing and cross-source verification to improve search accuracy for research, fact-checking, and information lookup tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruogu1992](https://clawhub.ai/user/ruogu1992) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to route search requests across multiple providers, compare results, mark agreement or disagreement, and return a confidence-scored summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms may be sent to multiple external search providers. <br>
Mitigation: Do not use the skill for secrets, private internal topics, regulated data, or queries that should not be shared with external search services. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ruogu1992/multi-search-fallback) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary with confidence score, key findings, source comparison table, and grouped raw results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include agreement, disagreement, and supplemental-result labels across search sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
