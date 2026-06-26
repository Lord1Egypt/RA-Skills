## Description: <br>
Queries TikTok Shop promotional videos for a product and returns engagement, estimated sales, GMV, creator, and publishing metadata for video marketing analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and commerce analysts use this skill to inspect TikTok product-associated videos, compare engagement and estimated conversion metrics, and identify influencer content that may be driving sales. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends TikTok product identifiers, optional influencer IDs, and API key-authenticated requests to LinkFox services. <br>
Mitigation: Use only with data that is appropriate to share with LinkFox and confirm the API key is scoped and stored as an environment variable. <br>
Risk: The skill instructs agents to automatically submit freeform interaction feedback to a separate LinkFox feedback API. <br>
Mitigation: Avoid including sensitive business details in feedback and obtain user or operator approval before sending feedback when appropriate. <br>
Risk: Persisted response files may contain sensitive commerce, pricing, or identifier data. <br>
Mitigation: Write response files outside git working trees and delete them after the task is complete. <br>


## Reference(s): <br>
- [EchoTik Product Video API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown tables, JSON API responses, shell commands, and optional persisted response files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY. Video sales and GMV are estimated values; persisted response files may contain sensitive commerce data and should be cleaned up after use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
