## Description: <br>
Fetches public Nature RSS and New Scientist Technology pages, filters for recent AI-related articles, and returns grouped summaries with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and researchers use this skill to ask an agent for a compact, source-labeled digest of recent AI-related articles from Nature and New Scientist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public source pages may change, and keyword filtering may include adjacent technology items or miss relevant AI articles. <br>
Mitigation: Review summaries and source links for accuracy before relying on the digest. <br>
Risk: The skill performs public web requests to Nature and New Scientist. <br>
Mitigation: Use it only in environments where fetching those public pages is acceptable. <br>


## Reference(s): <br>
- [Nature RSS feed](https://www.nature.com/nature.rss) <br>
- [New Scientist Technology](https://www.newscientist.com/subject/technology/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown digest grouped by source with headlines, one-sentence summaries, dates when available, and URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public web fetches and limits results to at most 7 items per source.] <br>

## Skill Version(s): <br>
1.9.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
