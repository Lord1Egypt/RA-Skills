## Description: <br>
Queries Zhihuiya patent bibliography data by patent ID or publication number and helps present patent metadata such as titles, applicants, inventors, classifications, citations, abstracts, and dates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve structured bibliography records for known patent IDs or publication numbers, then present only the requested metadata in tables or concise sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent IDs or publication numbers are sent to a LinkFox tool gateway for lookup. <br>
Mitigation: Use only when sharing those identifiers with LinkFox is acceptable for the user and organization. <br>
Risk: The artifact instructs agents to automatically send feedback, user intent, or conversation details to a separate feedback endpoint without clear user consent. <br>
Mitigation: Disable automatic feedback reporting or require explicit user consent before sending feedback or conversation details. <br>


## Reference(s): <br>
- [Zhihuiya Bibliography API Reference](artifact/references/api.md) <br>
- [Zhihuiya Bibliography on ClawHub](https://clawhub.ai/linkfox-ai/linkfox-zhihuiya-bibliography) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>
- [Zhihuiya Bibliography API Endpoint](https://tool-gateway.linkfox.com/zhihuiya/bibliography) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown tables or sections for users, with JSON returned by the helper script when run directly.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries require LINKFOXAGENT_API_KEY and accept up to 100 patent IDs or publication numbers per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
