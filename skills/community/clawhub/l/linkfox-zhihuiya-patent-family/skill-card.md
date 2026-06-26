## Description: <br>
Helps agents look up Zhihuiya (PatSnap) patent family data by patent ID or publication number and present Simple, INPADOC, and PatSnap family members. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and patent-focused teams use this skill to retrieve factual patent family members for known patent IDs or publication numbers, compare family definitions, and summarize family counts and jurisdictions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent identifiers are sent to LinkFox/Zhihuiya services with a LinkFox API key. <br>
Mitigation: Use the skill only for patent identifiers approved for sharing with those services, and manage LINKFOXAGENT_API_KEY in a controlled environment. <br>
Risk: Automatic feedback behavior may send user intent or request details to a separate LinkFox feedback endpoint without a clear consent step. <br>
Mitigation: Review or disable automatic feedback behavior before deployment, or require explicit user consent before sending feedback. <br>


## Reference(s): <br>
- [Zhihuiya Patent Family API Reference](references/api.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/linkfox-ai/linkfox-zhihuiya-patent-family) <br>
- [Zhihuiya Patent Family API Endpoint](https://tool-gateway.linkfox.com/zhihuiya/patentFamily) <br>
- [LinkFox Feedback API](https://skill-api.linkfox.com/api/v1/public/feedback) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries and tables with JSON request examples and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY. Accepts patentId or patentNumber, with comma-separated batches up to 100 entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
