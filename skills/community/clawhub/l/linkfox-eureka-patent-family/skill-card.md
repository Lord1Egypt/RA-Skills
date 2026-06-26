## Description: <br>
Guides agents to query patent family information through the Eureka patent data platform, including Simple Family, INPADOC Family, and PatSnap Family results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Patent analysts, IP researchers, and agents assisting external users use this skill to look up Simple, INPADOC, and PatSnap family members for known patent IDs or publication numbers and summarize family counts and jurisdictions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API key and sends patent IDs or publication numbers to the LinkFox Eureka patent-family API. <br>
Mitigation: Use a dedicated LinkFox API key and avoid submitting confidential patent strategy or sensitive research targets unless approved. <br>
Risk: The skill instructions ask the agent to submit conversation-derived feedback to a separate LinkFox feedback endpoint without interrupting the user's flow. <br>
Mitigation: Do not submit feedback unless the user explicitly consents, and minimize the content sent to the feedback API. <br>


## Reference(s): <br>
- [Eureka Patent Family API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-eureka-patent-family) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with JSON request examples and tabular patent-family summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; accepts patentId or patentNumber, with up to 100 comma-separated entries per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
