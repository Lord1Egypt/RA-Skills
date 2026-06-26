## Description: <br>
Retrieves translated patent titles and abstracts from the Eureka patent data platform using patent IDs or publication numbers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, patent researchers, and business users use this skill to look up translated patent titles and abstracts in Chinese, English, or Japanese for known patent IDs or publication numbers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent identifiers and lookup terms are sent to an external patent API. <br>
Mitigation: Use only data you are authorized to submit, and avoid confidential, unpublished, or client-sensitive research unless sharing it with the API is approved. <br>
Risk: The skill requires an API key for the LinkFox tool gateway. <br>
Mitigation: Store the API key in the LINKFOXAGENT_API_KEY environment variable and avoid pasting, logging, or sharing the credential. <br>
Risk: Results are limited to translated titles and abstracts and may use a family-patent abstract when explicitly requested. <br>
Mitigation: Verify results against authoritative patent records before using them for legal, IP, or business decisions, and clearly note family-patent substitutions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-eureka-abstract-translated) <br>
- [Eureka abstract translation API reference](references/api.md) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown tables and plain text, with optional JSON from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports batches of up to 100 patents per request and can return title, abstract, publication number, related-family publication number, and token cost.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
