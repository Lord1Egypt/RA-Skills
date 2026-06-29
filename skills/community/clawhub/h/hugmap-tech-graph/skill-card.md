## Description: <br>
Hugmap Tech News Graph queries HugMap's public, read-only technology knowledge graph for people, companies, technologies, products, papers, patents, articles, events, and their relationships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jones-so](https://clawhub.ai/user/jones-so) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to look up technology entities, explore relationship paths and graph neighborhoods, browse industry taxonomies, and summarize recent technology news from HugMap with source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and entity IDs are sent over the network to HugMap or to the configured HugMap-compatible endpoint. <br>
Mitigation: Avoid sensitive queries and leave HUGMAP_BASE_URL at the default HugMap site unless intentionally using another trusted endpoint. <br>
Risk: Knowledge graph results can be incomplete, outdated, or reflect HugMap's available source data. <br>
Mitigation: Preserve HugMap links in responses so readers can inspect full entity pages, relationship graphs, and source context. <br>


## Reference(s): <br>
- [HugMap](https://www.hugmap.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/jones-so/hugmap-tech-graph) <br>
- [HugMap Open API Endpoint Reference](artifact/reference.md) <br>
- [HugMap Usage Examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON from a Python CLI, with Markdown-ready HugMap entity links for agent responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3. Uses optional HUGMAP_BASE_URL to choose the HugMap API base URL; defaults to https://www.hugmap.com.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
