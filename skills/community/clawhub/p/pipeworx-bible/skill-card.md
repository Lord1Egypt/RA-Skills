## Description: <br>
Fetch Bible verses, passages, and random scripture from bible-api.com — multiple translations supported. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up Bible verses, passages, or random scripture for devotional, study, conversational, newsletter, or social content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bible lookup requests are routed through Pipeworx's remote MCP gateway. <br>
Mitigation: Use the skill only when that remote service is acceptable, and avoid sending private notes or sensitive context in lookup prompts. <br>
Risk: The connection example installs mcp-remote with @latest, which can reduce reproducibility. <br>
Mitigation: Pin mcp-remote to a reviewed version when reproducible installs are required. <br>


## Reference(s): <br>
- [Pipeworx Bible pack](https://pipeworx.io/packs/bible) <br>
- [Pipeworx Bible MCP gateway](https://gateway.pipeworx.io/bible/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Shell commands] <br>
**Output Format:** [Structured text with JSON MCP configuration and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the documented example and uses the Pipeworx remote MCP gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
