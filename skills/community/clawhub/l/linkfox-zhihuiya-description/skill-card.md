## Description: <br>
Retrieves patent description and specification data from the Zhihuiya patent database by patent ID or publication number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve and present full patent description text for one or more known patent IDs or publication numbers. It supports batch lookup and optional family-patent substitution when the requested description is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent identifiers and the LinkFox API key are sent to LinkFox/Zhihuiya. <br>
Mitigation: Use the skill only when those disclosures are acceptable, and avoid confidential patent research unless disclosure risk is controlled. <br>
Risk: The skill asks agents to submit automatic feedback to a separate provider endpoint without clear user consent. <br>
Mitigation: Require explicit approval before submitting any feedback to the separate feedback API. <br>


## Reference(s): <br>
- [Zhihuiya Patent Description API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-zhihuiya-description) <br>
- [LinkFox Tool Gateway Description Endpoint](https://tool-gateway.linkfox.com/zhihuiya/descriptionData) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with JSON request parameters, shell command examples, and structured patent-description results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires at least one patent ID or publication number; batch requests are limited to 100 identifiers and returned descriptions may be long.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
