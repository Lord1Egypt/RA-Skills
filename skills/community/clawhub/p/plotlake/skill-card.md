## Description: <br>
Subscribes to WeChat public accounts and other feed sources to retrieve raw articles for daily digest assembly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eggyrooch-blip](https://clawhub.ai/user/eggyrooch-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create Plotlake channels, subscribe to curated or manually supplied feed sources, and fetch article content for LLM-generated daily digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External API calls and submitted feed URLs may expose channel activity or sensitive private links to Plotlake. <br>
Mitigation: Use public RSS or website URLs, avoid sensitive private links, and confirm the data-sharing posture before adding sources. <br>
Risk: The skill includes DELETE commands for removing channel sources. <br>
Mitigation: Review the channel ID and source ID before running deletion commands. <br>
Risk: Fetched article content may be passed to an LLM for daily digest generation. <br>
Mitigation: Review copyright, privacy, and internal data-handling requirements before summarizing or redistributing fetched content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eggyrooch-blip/plotlake) <br>
- [Project homepage](https://github.com/eggyrooch-blip/wewerss) <br>
- [Plotlake Open Channel API](https://api.plotlake.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq; no API key environment variable is documented.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
