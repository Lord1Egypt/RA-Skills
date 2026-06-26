## Description: <br>
Collects, verifies, and ranks current news for a specified industry, then outputs Chinese summaries sorted by popularity with original source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alpzhang](https://clawhub.ai/user/alpzhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, analysts, and industry teams use this skill to gather recent public news for a target industry, filter out adjacent-industry noise, and prioritize stories by heat. It is especially suited to Chinese-language news digests that need source links, coverage counts, and transparent search coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public news pages can be incomplete, paywalled, outdated, or inaccurate. <br>
Mitigation: Verify important summaries against the original sources before relying on them. <br>
Risk: The workflow performs multiple web searches and page fetches for each request. <br>
Mitigation: Use it when current public-news collection is intended and review the final source list for coverage gaps. <br>


## Reference(s): <br>
- [Recommended Industry News Sources](references/sources.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/alpzhang/industry-news-collector) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Chinese Markdown news digest with ranked sections, source links, and collection statistics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 15-25 deduplicated public-news items sorted by heat, with brief summaries and original links when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
