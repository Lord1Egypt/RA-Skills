## Description: <br>
Retrieves patent PDF full-text download links from the Zhihuiya patent database by patent ID or publication number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve one or more patent PDF links from Zhihuiya by publication number or Zhihuiya patent ID, with optional family-patent substitution when the original PDF is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent identifiers and request details are sent to LinkFox's tool gateway when the skill retrieves PDF links. <br>
Mitigation: Use the skill only for patent identifiers that may be shared with LinkFox, and use a scoped or revocable LINKFOXAGENT_API_KEY where possible. <br>
Risk: The artifact instructs agents to automatically send feedback, including user intent or interaction details, to a separate LinkFox feedback endpoint. <br>
Mitigation: Disable or avoid automatic feedback submission unless the user explicitly approves what will be sent. <br>


## Reference(s): <br>
- [Zhihuiya PDF API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-zhihuiya-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables or lists with patent identifiers, PDF links, substitution notes, and error guidance; JSON when the bundled script is executed directly.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY for live API calls; supports up to 100 patent identifiers per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
