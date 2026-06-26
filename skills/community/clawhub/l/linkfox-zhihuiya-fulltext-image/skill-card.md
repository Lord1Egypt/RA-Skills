## Description: <br>
Retrieves patent fulltext image metadata, including drawing and diagram links, from the Zhihuiya patent data service by patent ID or publication number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Patent researchers, analysts, and developers use this skill to retrieve the drawings, figures, diagrams, and image download paths associated with a known patent ID or publication number. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent identifiers and publication numbers are sent to LinkFox for lookup. <br>
Mitigation: Use a dedicated LinkFox API key and confirm that sharing the requested patent identifiers with LinkFox is acceptable for the user's context. <br>
Risk: The artifact asks agents to report feedback and user context to a separate LinkFox feedback endpoint. <br>
Mitigation: Disable feedback submission or require explicit approval before sending feedback, and redact sensitive patent, business, or conversation details. <br>


## Reference(s): <br>
- [Zhihuiya Fulltext Image API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON API responses and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and at least one patentId or patentNumber; each request returns at most 100 images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
