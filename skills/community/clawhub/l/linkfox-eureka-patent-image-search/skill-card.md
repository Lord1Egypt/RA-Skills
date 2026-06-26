## Description: <br>
Performs single-image patent visual similarity searches on the Eureka patent platform for design and utility patents, with optional filters for patent authority, Locarno class, dates, legal status, assignee, keywords, sorting, and pagination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, patent searchers, and commerce teams use this skill to find visually similar design or utility patents from a publicly accessible product image URL. It helps configure the correct Eureka search model, filters, pagination, and result presentation for image-based patent discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox/Eureka API key and sends patent search filters plus the submitted image URL to a third-party service. <br>
Mitigation: Use only in trusted environments, store LINKFOXAGENT_API_KEY as a secret, rotate it if exposed, and avoid sending private, signed, intranet, confidential, or customer-sensitive image URLs. <br>
Risk: The artifact includes feedback behavior that can send interaction details to a separate LinkFox endpoint. <br>
Mitigation: Send feedback only after explicit user consent and keep feedback content minimal. <br>
Risk: Image searches depend on a publicly accessible URL and third-party service availability. <br>
Mitigation: Confirm the image is intended for external sharing and treat failed searches or unavailable endpoints as non-authoritative. <br>


## Reference(s): <br>
- [Eureka Patent Image Search API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-eureka-patent-image-search) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API responses and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and a single publicly accessible image URL; results include patent metadata, image URLs, similarity scores, counts, and pagination fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
