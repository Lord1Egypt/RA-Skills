## Description: <br>
Retrieves patent abstract drawings from the Zhihuiya patent database by patent ID or publication number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up patent abstract images for one or more patent IDs or publication numbers and present the returned image paths with patent metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent identifiers are sent to the LinkFox/Zhihuiya API for lookup. <br>
Mitigation: Use a dedicated LinkFox API key and submit only patent identifiers that are approved for third-party processing. <br>
Risk: The skill text asks agents to automatically submit interaction feedback to a separate LinkFox endpoint. <br>
Mitigation: Require explicit user approval before calling the feedback API, or disable feedback submission in deployments where automatic reporting is not allowed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-zhihuiya-abstract-image) <br>
- [Zhihuiya Abstract Image API Reference](references/api.md) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>
- [LinkFox Tool Gateway Abstract Image API](https://tool-gateway.linkfox.com/zhihuiya/abstractImage) <br>
- [LinkFox Feedback API](https://skill-api.linkfox.com/api/v1/public/feedback) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline image links, tables or lists, JSON examples, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and accepts patentId or patentNumber values, with batch queries up to 100 comma-separated patents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
