## Description: <br>
Aggregates and ranks AI and technology news from a bundled source list, filtering for recent articles and returning summaries with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to compile a recent AI and technology news digest from a maintained list of public sources. It is intended for source-list-driven news aggregation, not generic web search or single-article lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public news sites can rate-limit, block, or return stale content. <br>
Mitigation: Review the bundled source list before use and rely on the skill's skipped-source reporting to identify blocked, stale, or unavailable sources. <br>
Risk: If all listed sources are blocked, the skill may fall back to broader web search. <br>
Mitigation: Confirm that fallback results still include source links and recent publication timing before relying on the digest. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/more-news) <br>
- [Bundled source list](artifact/source.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown news digest with ranked article summaries, source links, and a source-fetch summary table.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes skipped-source counts and reasons when sources are blocked, stale, or unavailable.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
